from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from accounts.models import AGE_GROUPS, SPOKEN_LANGUAGES, User
from learning.models import Enrollment, QuizResult, Topic

from .models import Connection, Message, MoodEntry

MAX_MESSAGE_LENGTH = 2000


def verified_psychologists():
    return User.objects.filter(role=User.Role.PSYCHOLOGIST, is_verified=True, is_active=True).annotate(
        topic_count=Count("topics", filter=Q(topics__is_published=True), distinct=True),
        client_count=Count("psychologist_connections", filter=Q(psychologist_connections__status="active"), distinct=True),
    )


def open_connection(client, psychologist):
    return Connection.objects.filter(
        client=client, psychologist=psychologist, status__in=[Connection.Status.PENDING, Connection.Status.ACTIVE]
    ).first()


def psychologist_list(request):
    qs = verified_psychologists()
    age = request.GET.get("age", "")
    if not age and request.user.is_authenticated and getattr(request.user, "age_group", ""):
        age = request.user.age_group
    lang = request.GET.get("lang", "")
    q = request.GET.get("q", "").strip()
    if age in dict(AGE_GROUPS):
        qs = qs.filter(age_groups__contains=age)
    if lang in dict(SPOKEN_LANGUAGES):
        qs = qs.filter(spoken_languages__contains=lang)
    if q:
        qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(specialization__icontains=q) | Q(bio__icontains=q))
    my_ids = set()
    if request.user.is_authenticated:
        my_ids = set(
            Connection.objects.filter(client=request.user, status__in=["pending", "active"]).values_list("psychologist_id", flat=True)
        )
    return render(
        request,
        "care/psychologists.html",
        {
            "psychologists": qs.order_by("-accepts_clients", "-topic_count", "first_name"),
            "age_groups": AGE_GROUPS,
            "languages": SPOKEN_LANGUAGES,
            "active_age": age,
            "active_lang": lang,
            "q": q,
            "my_ids": my_ids,
        },
    )


def psychologist_detail(request, username):
    psychologist = get_object_or_404(verified_psychologists(), username=username)
    connection = None
    if request.user.is_authenticated:
        connection = open_connection(request.user, psychologist)
    return render(
        request,
        "care/psychologist_detail.html",
        {
            "p": psychologist,
            "topics": Topic.objects.published().filter(author=psychologist).select_related("category"),
            "connection": connection,
        },
    )


@login_required
@require_POST
def choose(request, username):
    psychologist = get_object_or_404(verified_psychologists(), username=username)
    if not request.user.is_client:
        messages.error(request, _("Only clients can choose a psychologist."))
        return redirect("care:psychologist", username=username)
    existing = open_connection(request.user, psychologist)
    if existing:
        return redirect("care:chat", pk=existing.pk)
    if not psychologist.accepts_clients:
        messages.error(request, _("This psychologist is not accepting new clients right now."))
        return redirect("care:psychologist", username=username)
    concern = request.POST.get("concern", "").strip()[:MAX_MESSAGE_LENGTH]
    connection = Connection.objects.create(client=request.user, psychologist=psychologist, concern=concern)
    if concern:
        Message.objects.create(connection=connection, sender=request.user, text=concern)
    messages.success(request, _("Request sent! %(name)s will reply soon.") % {"name": psychologist.display_name})
    return redirect("care:chat", pk=connection.pk)


def _connections_for(user):
    return Connection.objects.filter(Q(client=user) | Q(psychologist=user)).select_related("client", "psychologist")


@login_required
def inbox(request):
    connections = list(_connections_for(request.user))
    for c in connections:
        c.partner = c.other(request.user)
        c.last = c.messages.order_by("-created_at").first()
        c.unread = c.unread_for(request.user)
    return render(request, "care/inbox.html", {"connections": connections})


def _get_connection(request, pk):
    connection = get_object_or_404(_connections_for(request.user), pk=pk)
    return connection


def _mark_read(connection, user):
    connection.messages.filter(read_at__isnull=True).exclude(sender=user).update(read_at=timezone.now())


def _render_messages(request, items):
    return "".join(render_to_string("care/_message.html", {"m": m, "user": request.user}, request=request) for m in items)


def mood_series(user, days=14):
    today = timezone.localdate()
    entries = {e.date: e for e in MoodEntry.objects.filter(user=user, date__gt=today - timedelta(days=days))}
    return [{"date": today - timedelta(days=i), "entry": entries.get(today - timedelta(days=i))} for i in range(days - 1, -1, -1)]


@login_required
def chat(request, pk):
    connection = _get_connection(request, pk)
    _mark_read(connection, request.user)
    items = connection.messages.select_related("sender", "topic")
    context = {
        "c": connection,
        "partner": connection.other(request.user),
        "items": items,
        "last_id": items.last().pk if items else 0,
        "is_psychologist_side": request.user.pk == connection.psychologist_id,
    }
    if context["is_psychologist_side"] and connection.status == Connection.Status.ACTIVE:
        client = connection.client
        context.update(
            client_enrollments=Enrollment.objects.filter(user=client).select_related("topic"),
            client_results=QuizResult.objects.filter(enrollment__user=client).select_related("step", "step__topic")[:6],
            client_moods=mood_series(client),
            recommend_topics=Topic.objects.published().order_by("title"),
        )
    return render(request, "care/chat.html", context)


@login_required
@require_POST
def send(request, pk):
    connection = _get_connection(request, pk)
    if not connection.is_open:
        return HttpResponseForbidden(_("This conversation is closed."))
    text = request.POST.get("text", "").strip()[:MAX_MESSAGE_LENGTH]
    topic = None
    if request.POST.get("topic") and request.user.pk == connection.psychologist_id:
        topic = Topic.objects.published().filter(pk=request.POST["topic"]).first()
    if not text and not topic:
        if request.headers.get("x-requested-with") == "fetch":
            return JsonResponse({"error": "empty"}, status=400)
        return redirect("care:chat", pk=pk)
    message = Message.objects.create(connection=connection, sender=request.user, text=text, topic=topic)
    connection.save(update_fields=["updated_at"])
    if request.headers.get("x-requested-with") == "fetch":
        return JsonResponse({"html": _render_messages(request, [message]), "last_id": message.pk})
    return redirect("care:chat", pk=pk)


@login_required
def poll(request, pk):
    connection = _get_connection(request, pk)
    try:
        after = int(request.GET.get("after", 0))
    except ValueError:
        after = 0
    items = list(connection.messages.filter(pk__gt=after).select_related("sender", "topic"))
    _mark_read(connection, request.user)
    return JsonResponse(
        {
            "html": _render_messages(request, items),
            "last_id": items[-1].pk if items else after,
            "status": connection.status,
        }
    )


@login_required
@require_POST
def respond(request, pk):
    connection = _get_connection(request, pk)
    action = request.POST.get("action")
    is_psych = request.user.pk == connection.psychologist_id
    if action in ("accept", "decline") and is_psych and connection.status == Connection.Status.PENDING:
        connection.status = Connection.Status.ACTIVE if action == "accept" else Connection.Status.DECLINED
        connection.save()
        note = _("I accepted your request. Let's work together!") if action == "accept" else _("Sorry, I can't take this request right now.")
        Message.objects.create(connection=connection, sender=request.user, text=note)
    elif action == "end" and connection.is_open:
        connection.status = Connection.Status.ENDED
        connection.save()
        messages.info(request, _("The conversation was closed."))
    else:
        raise Http404
    return redirect("care:chat", pk=pk)


@login_required
@require_POST
def mood(request):
    try:
        value = int(request.POST.get("mood", ""))
    except ValueError:
        value = 0
    if value not in MoodEntry.EMOJI:
        return JsonResponse({"error": "invalid"}, status=400)
    MoodEntry.objects.update_or_create(
        user=request.user, date=timezone.localdate(), defaults={"mood": value, "note": request.POST.get("note", "")[:200]}
    )
    if request.headers.get("x-requested-with") == "fetch":
        return JsonResponse({"ok": True, "emoji": MoodEntry.EMOJI[value]})
    messages.success(request, _("Thanks! Your mood is saved."))
    return redirect("accounts:dashboard")
