from datetime import datetime, timedelta
from datetime import timezone as dt_timezone
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from . import ai
from .models import Category, Enrollment, QuizResult, Reflection, Reminder, Step, StepCompletion, Topic


def catalog(request):
    topics = (
        Topic.objects.published()
        .select_related("category", "author")
        .annotate(step_count=Count("steps", distinct=True), learner_count=Count("enrollments", distinct=True))
    )
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    level = request.GET.get("level", "")
    if q:
        topics = topics.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(tags__icontains=q))
    if category:
        topics = topics.filter(category__slug=category)
    if level:
        topics = topics.filter(level=level)
    return render(
        request,
        "learning/catalog.html",
        {
            "topics": topics,
            "categories": Category.objects.all(),
            "levels": Topic.Level.choices,
            "q": q,
            "active_category": category,
            "active_level": level,
        },
    )


def _can_view(request, topic):
    """Drafts are visible only to their author and platform admins (for previewing)."""
    return topic.is_published or topic.author_id == request.user.pk or request.user.is_superuser


def _visible_topic(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    if not _can_view(request, topic):
        raise Http404
    return topic


def practice(request):
    """All tests and games across published topics, so people can jump straight in."""
    steps = list(
        Step.objects.filter(topic__is_published=True, kind__in=(Step.Kind.QUIZ, *Step.GAME_KINDS))
        .select_related("topic", "topic__category")
        .annotate(question_count=Count("questions"))
        .order_by("kind", "topic__title")
    )
    done_ids, scores = set(), {}
    if request.user.is_authenticated:
        done_ids = set(StepCompletion.objects.filter(enrollment__user=request.user).values_list("step_id", flat=True))
        for r in QuizResult.objects.filter(enrollment__user=request.user).order_by("created_at"):
            scores[r.step_id] = r.percent
    for s in steps:
        s.done = s.id in done_ids
        s.score = scores.get(s.id)
    return render(
        request,
        "learning/practice.html",
        {
            "tests": [s for s in steps if s.kind == Step.Kind.QUIZ],
            "games": [s for s in steps if s.kind in Step.GAME_KINDS],
            "total": len(steps),
        },
    )


def topic_detail(request, slug):
    topic = get_object_or_404(Topic.objects.select_related("category", "author"), slug=slug)
    if not _can_view(request, topic):
        raise Http404
    enrollment = None
    done_ids = set()
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, topic=topic).first()
        if enrollment:
            done_ids = enrollment.completed_step_ids
    return render(
        request,
        "learning/topic_detail.html",
        {
            "topic": topic,
            "steps": topic.steps.all(),
            "enrollment": enrollment,
            "done_ids": done_ids,
            "related": topic.related(limit=3),
            "learners": topic.enrollments.count(),
        },
    )


@login_required
@require_POST
def start(request, slug):
    topic = _visible_topic(request, slug)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, topic=topic)
    if not created:
        enrollment.touch()
    step = enrollment.next_step() or topic.steps.first()
    if step is None:
        messages.info(request, _("This topic has no steps yet."))
        return redirect(topic)
    return redirect("learning:step", slug=topic.slug, order=step.order)


def _get_enrollment(request, topic):
    enrollment, _created = Enrollment.objects.get_or_create(user=request.user, topic=topic)
    return enrollment


@login_required
def step_view(request, slug, order):
    topic = _visible_topic(request, slug)
    steps = list(topic.steps.all())
    step = next((s for s in steps if s.order == order), None)
    if step is None:
        raise Http404
    enrollment = _get_enrollment(request, topic)
    done_ids = enrollment.completed_step_ids

    index = steps.index(step)
    context = {
        "topic": topic,
        "step": step,
        "steps": steps,
        "index": index + 1,
        "total": len(steps),
        "prev_step": steps[index - 1] if index > 0 else None,
        "next_step": steps[index + 1] if index + 1 < len(steps) else None,
        "done_ids": done_ids,
        "is_done": step.id in done_ids,
        "progress": round(100 * len(done_ids) / len(steps)) if steps else 0,
        "ai_enabled": ai.is_enabled(),
    }
    if step.kind in (Step.Kind.QUIZ, Step.Kind.SCENARIO):
        context["questions"] = step.questions.all()
    if step.kind == Step.Kind.QUIZ:
        result = QuizResult.objects.filter(enrollment=enrollment, step=step).first()
        if result and request.GET.get("retake") != "1":
            band, text = step.interpret(result.score, result.max_score)
            context.update(result=result, result_text=text)
    elif step.kind == Step.Kind.REFLECTION:
        context["reflection"] = Reflection.objects.filter(enrollment=enrollment, step=step).first()
    return render(request, "learning/step.html", context)


@login_required
@require_POST
def step_submit(request, slug, order):
    topic = _visible_topic(request, slug)
    step = get_object_or_404(Step, topic=topic, order=order)
    enrollment = _get_enrollment(request, topic)

    if step.kind == Step.Kind.QUIZ:
        questions = list(step.questions.all())
        score, answers = 0, {}
        for question in questions:
            raw = request.POST.get(f"q{question.id}")
            options = question.option_list
            try:
                chosen = options[int(raw)]
            except (TypeError, ValueError, IndexError):
                messages.error(request, _("Please answer every question."))
                return redirect("learning:step", slug=slug, order=order)
            score += chosen["points"]
            answers[str(question.id)] = chosen["index"]
        max_score = sum(q.max_points for q in questions)
        band, _text = step.interpret(score, max_score)
        QuizResult.objects.create(enrollment=enrollment, step=step, score=score, max_score=max_score, band=band, answers=answers)
        _complete(enrollment, step)
        return redirect("learning:step", slug=slug, order=order)

    if step.kind == Step.Kind.REFLECTION:
        text = request.POST.get("text", "").strip()
        if len(text) < 3:
            messages.error(request, _("Write a few words — it is only for you and your psychologist."))
            return redirect("learning:step", slug=slug, order=order)
        feedback = ""
        if request.POST.get("ai") == "1" and ai.quota_left(request.user) <= 0:
            messages.warning(request, _("You have used today's AI feedback limit. Your answer was saved."))
        elif request.POST.get("ai") == "1":
            feedback = ai.reflection_feedback(
                topic_title=topic.title, question=step.body, answer=text, language=get_language()
            ) or ""
            if not feedback:
                messages.warning(request, _("AI feedback is unavailable right now, but your answer was saved."))
        Reflection.objects.create(enrollment=enrollment, step=step, text=text, ai_feedback=feedback)
        _complete(enrollment, step)
        return redirect("learning:step", slug=slug, order=order)

    _complete(enrollment, step)
    return _go_next(enrollment, topic)


@login_required
def continue_topic(request, slug):
    topic = _visible_topic(request, slug)
    return _go_next(_get_enrollment(request, topic), topic)


def _complete(enrollment, step):
    StepCompletion.objects.get_or_create(enrollment=enrollment, step=step)
    enrollment.last_activity = timezone.now()
    if enrollment.next_step() is None and enrollment.status != Enrollment.Status.COMPLETED:
        enrollment.status = Enrollment.Status.COMPLETED
        enrollment.completed_at = timezone.now()
        Reminder.objects.filter(user=enrollment.user, topic=enrollment.topic, is_done=False).update(is_done=True)
    enrollment.save()


def _go_next(enrollment, topic):
    step = enrollment.next_step()
    if step is None:
        return redirect("learning:finish", slug=topic.slug)
    return redirect("learning:step", slug=topic.slug, order=step.order)


@login_required
def finish(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, topic=topic)
    if enrollment.status != Enrollment.Status.COMPLETED:
        return _go_next(enrollment, topic)
    taken = Enrollment.objects.filter(user=request.user).values_list("topic_id", flat=True)
    return render(
        request,
        "learning/finish.html",
        {
            "topic": topic,
            "enrollment": enrollment,
            "results": enrollment.quiz_results.select_related("step"),
            "reflections": enrollment.reflections.select_related("step"),
            "related": topic.related(limit=3, exclude_ids=taken),
        },
    )


@login_required
@require_POST
def pause(request, slug):
    """User leaves a topic midway and picks when to be reminded to come back."""
    topic = get_object_or_404(Topic.objects.published(), slug=slug)
    raw = request.POST.get("remind_at", "")
    try:
        remind_at = timezone.make_aware(datetime.strptime(raw, "%Y-%m-%dT%H:%M"))
    except ValueError:
        remind_at = timezone.now() + timedelta(days=1)
    if remind_at <= timezone.now():
        messages.error(request, _("Please choose a time in the future."))
        next_url = request.POST.get("next", "")
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next_url = topic.get_absolute_url()
        return redirect(next_url)
    _get_enrollment(request, topic).touch()
    reminder = Reminder.objects.create(user=request.user, topic=topic, remind_at=remind_at, note=request.POST.get("note", "")[:200])
    messages.success(
        request,
        _("Saved! We will remind you on %(when)s. Add it to your phone calendar from the dashboard.")
        % {"when": timezone.localtime(reminder.remind_at).strftime("%d.%m.%Y %H:%M")},
    )
    return redirect("accounts:dashboard")


def _reminder_text(reminder):
    title = _("Ruhiyat: continue “%(topic)s”") % {"topic": reminder.topic.title}
    link = settings.SITE_URL + reminder.topic.get_absolute_url()
    return title, link


@login_required
def reminder_ics(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    title, link = _reminder_text(reminder)
    start = reminder.remind_at.astimezone(dt_timezone.utc)
    end = start + timedelta(minutes=reminder.topic.duration_minutes or 15)
    fmt = "%Y%m%dT%H%M%SZ"

    def esc(value):
        return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

    body = "\r\n".join(
        [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Ruhiyat//Reminders//EN",
            "BEGIN:VEVENT",
            f"UID:ruhiyat-reminder-{reminder.pk}@ruhiyat",
            f"DTSTAMP:{timezone.now().astimezone(start.tzinfo):{fmt}}",
            f"DTSTART:{start:{fmt}}",
            f"DTEND:{end:{fmt}}",
            f"SUMMARY:{esc(title)}",
            f"DESCRIPTION:{esc(link)}",
            f"URL:{link}",
            "BEGIN:VALARM",
            "TRIGGER:-PT10M",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{esc(title)}",
            "END:VALARM",
            "END:VEVENT",
            "END:VCALENDAR",
            "",
        ]
    )
    response = HttpResponse(body, content_type="text/calendar; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="ruhiyat-{reminder.topic.slug}.ics"'
    return response


@login_required
def reminder_google(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    title, link = _reminder_text(reminder)
    start = reminder.remind_at.astimezone(dt_timezone.utc)
    end = start + timedelta(minutes=reminder.topic.duration_minutes or 15)
    params = urlencode(
        {
            "action": "TEMPLATE",
            "text": title,
            "dates": f"{start:%Y%m%dT%H%M%SZ}/{end:%Y%m%dT%H%M%SZ}",
            "details": link,
        }
    )
    return redirect(f"https://calendar.google.com/calendar/render?{params}")


@login_required
@require_POST
def reminder_done(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.is_done = True
    reminder.save(update_fields=["is_done"])
    if request.POST.get("go") == "1":
        return redirect("learning:continue", slug=reminder.topic.slug)
    return redirect("accounts:dashboard")
