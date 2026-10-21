from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language

from care.models import Connection, Message
from learning.models import Reminder

LANGUAGE_FLAGS = {"uz": "UZ", "kaa": "QQ", "ru": "RU", "en": "EN"}


def site(request):
    current = get_language()
    due = unread = 0
    if request.user.is_authenticated:
        user = request.user
        due = Reminder.objects.filter(user=user, is_done=False, remind_at__lte=timezone.now()).count()
        unread = (
            Message.objects.filter(Q(connection__client=user) | Q(connection__psychologist=user), read_at__isnull=True)
            .exclude(sender=user)
            .count()
        )
        if user.is_psychologist:
            unread += Connection.objects.filter(psychologist=user, status=Connection.Status.PENDING, messages__isnull=True).count()
    return {
        "site_languages": [
            {"code": code, "name": name, "short": LANGUAGE_FLAGS.get(code, code.upper()), "active": code == current}
            for code, name in settings.LANGUAGES
        ],
        "current_language_short": LANGUAGE_FLAGS.get(current, (current or "").upper()),
        "due_reminders_count": due,
        "unread_messages_count": unread,
    }
