import calendar
from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from care.models import Connection, MoodEntry
from care.views import mood_series, verified_psychologists
from learning.models import Enrollment, QuizResult, Reflection, Reminder, StepCompletion, Topic

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    form = RegisterForm(request.POST or None, initial={"role": request.GET.get("role", User.Role.CLIENT)})
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        if user.is_psychologist:
            # Sensible starting point; they refine it in their profile.
            user.spoken_languages = get_language() or "uz"
            user.age_group = ""
        user.save()
        login(request, user)
        if user.is_psychologist:
            messages.info(request, _("Welcome! An administrator will verify your profile so you can publish topics."))
        else:
            messages.success(request, _("Welcome to Ruhiyat! Choose your first topic."))
        return redirect("accounts:dashboard")
    return render(request, "accounts/register.html", {"form": form})


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Profile saved."))
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser or user.role == User.Role.ADMIN:
        return redirect("admin:index")
    if user.is_psychologist:
        return psychologist_dashboard(request)
    return client_dashboard(request)


def month_grid(request, user):
    today = timezone.localdate()
    try:
        year, month = (int(x) for x in request.GET.get("month", "").split("-"))
        first = date(year, month, 1)
    except ValueError:
        first = today.replace(day=1)
    weeks = calendar.Calendar(firstweekday=0).monthdatescalendar(first.year, first.month)
    start, end = weeks[0][0], weeks[-1][-1]

    reminder_days = {}
    for r in Reminder.objects.filter(user=user, is_done=False).select_related("topic"):
        reminder_days.setdefault(timezone.localtime(r.remind_at).date(), []).append(r)
    active_days = {
        timezone.localtime(ts).date()
        for ts in StepCompletion.objects.filter(
            enrollment__user=user, completed_at__date__gte=start, completed_at__date__lte=end
        ).values_list("completed_at", flat=True)
    }
    prev_month = (first.replace(day=1) - timedelta(days=1)).replace(day=1)
    next_month = (first.replace(day=28) + timedelta(days=4)).replace(day=1)
    return {
        "first": first,
        "today": today,
        "weeks": [
            [
                {
                    "date": d,
                    "in_month": d.month == first.month,
                    "reminders": reminder_days.get(d, []),
                    "active": d in active_days,
                }
                for d in week
            ]
            for week in weeks
        ],
        "prev": prev_month.strftime("%Y-%m"),
        "next": next_month.strftime("%Y-%m"),
    }


def client_dashboard(request):
    user = request.user
    enrollments = list(Enrollment.objects.filter(user=user).select_related("topic", "topic__category", "topic__author"))
    enrolled_ids = [e.topic_id for e in enrollments]
    in_progress = [e for e in enrollments if e.status == Enrollment.Status.ACTIVE and not e.is_abandoned]
    abandoned = [e for e in enrollments if e.is_abandoned]
    for e in abandoned:
        e.suggestions = e.topic.related(limit=2, exclude_ids=enrolled_ids)
    completed = [e for e in enrollments if e.status == Enrollment.Status.COMPLETED]
    reminders = Reminder.objects.filter(user=user, is_done=False).select_related("topic")
    recommended = Topic.objects.published().exclude(pk__in=enrolled_ids).select_related("category", "author")[:3]
    connections = list(
        Connection.objects.filter(client=user, status__in=["pending", "active"]).select_related("psychologist")
    )
    for c in connections:
        c.unread = c.unread_for(user)
    suggested = []
    if not connections:
        suggested = verified_psychologists().filter(accepts_clients=True)
        if user.age_group:
            suggested = suggested.filter(age_groups__contains=user.age_group)
        suggested = suggested.order_by("-topic_count")[:3]
    stats = {
        "steps": StepCompletion.objects.filter(enrollment__user=user).count(),
        "completed": len(completed),
        "tests": QuizResult.objects.filter(enrollment__user=user).count(),
        "reflections": Reflection.objects.filter(enrollment__user=user).count(),
    }
    return render(
        request,
        "accounts/dashboard_client.html",
        {
            "in_progress": in_progress,
            "abandoned": abandoned,
            "completed": completed,
            "due_reminders": [r for r in reminders if r.is_due],
            "upcoming_reminders": [r for r in reminders if not r.is_due][:5],
            "recommended": recommended,
            "stats": stats,
            "cal": month_grid(request, user),
            "connections": connections,
            "suggested_psychologists": suggested,
            "today_mood": MoodEntry.objects.filter(user=user, date=timezone.localdate()).first(),
            "moods": mood_series(user),
            "mood_choices": [(v, label, MoodEntry.EMOJI[v]) for v, label in MoodEntry.MOODS],
        },
    )


def psychologist_dashboard(request):
    user = request.user
    topics = (
        Topic.objects.filter(author=user)
        .select_related("category")
        .annotate(
            learners=Count("enrollments", distinct=True),
            finished=Count("enrollments", filter=Q(enrollments__status=Enrollment.Status.COMPLETED), distinct=True),
            step_count=Count("steps", distinct=True),
        )
    )
    cutoff = timezone.now() - timedelta(days=settings.ABANDON_AFTER_DAYS)
    abandoned = Enrollment.objects.filter(topic__author=user, status=Enrollment.Status.ACTIVE, last_activity__lt=cutoff).count()
    results = QuizResult.objects.filter(step__topic__author=user).select_related("enrollment__user", "step__topic")[:8]
    reflections = Reflection.objects.filter(step__topic__author=user).select_related("enrollment__user", "step__topic")[:8]
    requests_ = Connection.objects.filter(psychologist=user, status=Connection.Status.PENDING).select_related("client")
    clients = list(Connection.objects.filter(psychologist=user, status=Connection.Status.ACTIVE).select_related("client"))
    for c in clients:
        c.unread = c.unread_for(user)
        c.last_mood = MoodEntry.objects.filter(user=c.client).first()
        c.progress = Enrollment.objects.filter(user=c.client).count()
    total_learners = sum(t.learners for t in topics)
    total_finished = sum(t.finished for t in topics)
    avg = QuizResult.objects.filter(step__topic__author=user).aggregate(a=Avg("score"), m=Avg("max_score"))
    return render(
        request,
        "accounts/dashboard_psychologist.html",
        {
            "topics": topics,
            "results": results,
            "reflections": reflections,
            "requests": requests_,
            "clients": clients,
            "profile_incomplete": not (user.age_groups and user.spoken_languages and user.bio),
            "stats": {
                "topics": len(topics),
                "clients": len(clients),
                "learners": total_learners,
                "completion": round(100 * total_finished / total_learners) if total_learners else 0,
                "abandoned": abandoned,
                "avg_score": round(100 * avg["a"] / avg["m"]) if avg["a"] and avg["m"] else 0,
            },
        },
    )

