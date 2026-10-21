from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Connection(models.Model):
    """A client chose a psychologist; once accepted they can chat and the psychologist sees progress."""

    class Status(models.TextChoices):
        PENDING = "pending", _("Waiting for reply")
        ACTIVE = "active", _("Active")
        DECLINED = "declined", _("Declined")
        ENDED = "ended", _("Ended")

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_connections")
    psychologist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="psychologist_connections")
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    concern = models.TextField(_("what the client wants help with"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = _("client–psychologist link")
        verbose_name_plural = _("Client–psychologist links")
        constraints = [
            models.UniqueConstraint(
                fields=["client", "psychologist"],
                condition=models.Q(status__in=["pending", "active"]),
                name="one_open_connection_per_pair",
            )
        ]

    def __str__(self):
        return f"{self.client} ↔ {self.psychologist} ({self.status})"

    @property
    def is_open(self):
        return self.status in (self.Status.PENDING, self.Status.ACTIVE)

    def other(self, user):
        return self.psychologist if user.pk == self.client_id else self.client

    def unread_for(self, user):
        return self.messages.filter(read_at__isnull=True).exclude(sender=user).count()


class Message(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField(_("message"), blank=True)
    # A psychologist can recommend a topic; it renders as a card in the chat.
    topic = models.ForeignKey("learning.Topic", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name = _("message")
        verbose_name_plural = _("Messages")


class MoodEntry(models.Model):
    MOODS = [
        (1, _("Very bad")),
        (2, _("Bad")),
        (3, _("Okay")),
        (4, _("Good")),
        (5, _("Great")),
    ]
    EMOJI = {1: "😣", 2: "😕", 3: "😐", 4: "🙂", 5: "😄"}

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="moods")
    date = models.DateField(default=timezone.localdate)
    mood = models.PositiveSmallIntegerField(_("mood"), choices=MOODS)
    note = models.CharField(_("note"), max_length=200, blank=True)

    class Meta:
        ordering = ["-date"]
        unique_together = [("user", "date")]
        verbose_name = _("mood check-in")
        verbose_name_plural = _("Mood check-ins")

    @property
    def emoji(self):
        return self.EMOJI[self.mood]
