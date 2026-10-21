from datetime import timedelta

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

COLOR_CHOICES = [
    ("violet", _("Violet")),
    ("ocean", _("Ocean")),
    ("sunset", _("Sunset")),
    ("mint", _("Mint")),
    ("rose", _("Rose")),
    ("amber", _("Amber")),
]


def unique_slug(instance, value, max_length=80):
    base = slugify(value)[:max_length] or "item"
    slug, n = base, 2
    model = type(instance)
    while model.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f"{base[: max_length - 4]}-{n}"
        n += 1
    return slug


class Category(models.Model):
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"), max_length=100, unique=True, blank=True)
    icon = models.CharField(_("icon (emoji)"), max_length=8, default="✨")
    color = models.CharField(_("color"), max_length=20, choices=COLOR_CHOICES, default="violet")
    order = models.PositiveSmallIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name_en or self.name)
        super().save(*args, **kwargs)


class TopicQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class Topic(models.Model):
    class Level(models.TextChoices):
        BEGINNER = "beginner", _("Beginner")
        INTERMEDIATE = "intermediate", _("Intermediate")
        ADVANCED = "advanced", _("Advanced")

    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.PROTECT, related_name="topics")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("psychologist"),
        on_delete=models.CASCADE,
        related_name="topics",
        limit_choices_to={"role": "psychologist"},
    )
    title = models.CharField(_("title"), max_length=160)
    slug = models.SlugField(_("slug"), max_length=90, unique=True, blank=True)
    summary = models.CharField(_("short summary"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    goal = models.CharField(_("what you will achieve"), max_length=255, blank=True)
    icon = models.CharField(_("icon (emoji)"), max_length=8, default="🧠")
    color = models.CharField(_("color"), max_length=20, choices=COLOR_CHOICES, default="violet")
    level = models.CharField(_("level"), max_length=20, choices=Level.choices, default=Level.BEGINNER)
    duration_minutes = models.PositiveSmallIntegerField(_("duration (minutes)"), default=15)
    tags = models.CharField(_("tags"), max_length=200, blank=True, help_text=_("Comma separated, used to suggest related topics."))
    is_published = models.BooleanField(_("published"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TopicQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("topic")
        verbose_name_plural = _("Topics")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title_en or self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("learning:topic", args=[self.slug])

    @property
    def tag_list(self):
        return [t.strip().lower() for t in self.tags.split(",") if t.strip()]

    def related(self, limit=3, exclude_ids=()):
        """Topics sharing a tag or the category, most similar first."""
        candidates = Topic.objects.published().exclude(pk=self.pk).exclude(pk__in=exclude_ids).select_related("category", "author")
        tags = set(self.tag_list)

        def score(t):
            return len(tags & set(t.tag_list)) * 2 + (t.category_id == self.category_id)

        ranked = sorted(candidates, key=score, reverse=True)
        return [t for t in ranked if score(t) > 0][:limit] or ranked[:limit]


class Step(models.Model):
    class Kind(models.TextChoices):
        LESSON = "lesson", _("Lesson")
        QUIZ = "quiz", _("Test")
        REFLECTION = "reflection", _("Reflection")
        BREATHING = "breathing", _("Breathing game")
        CARDS = "cards", _("Flip cards game")
        SCENARIO = "scenario", _("Situation game")

    GAME_KINDS = ("breathing", "cards", "scenario")

    topic = models.ForeignKey(Topic, verbose_name=_("topic"), on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveSmallIntegerField(_("order"), default=1)
    kind = models.CharField(_("type"), max_length=20, choices=Kind.choices, default=Kind.LESSON)
    title = models.CharField(_("title"), max_length=160)
    body = models.TextField(
        _("content"),
        blank=True,
        help_text=_(
            "Lesson: text (blank line = new paragraph). Reflection: the question. "
            "Cards: one card per line as “front | back”. Situation game: an introduction; "
            "situations are added as questions."
        ),
    )
    # Breathing game timings (seconds).
    inhale_seconds = models.PositiveSmallIntegerField(_("inhale (s)"), default=4)
    hold_seconds = models.PositiveSmallIntegerField(_("hold (s)"), default=4)
    exhale_seconds = models.PositiveSmallIntegerField(_("exhale (s)"), default=6)
    cycles = models.PositiveSmallIntegerField(_("cycles"), default=4)
    # Quiz interpretation by score share: < 40% low, < 75% medium, otherwise high.
    result_low = models.TextField(_("result: low score"), blank=True)
    result_mid = models.TextField(_("result: medium score"), blank=True)
    result_high = models.TextField(_("result: high score"), blank=True)

    class Meta:
        ordering = ["topic", "order", "id"]
        verbose_name = _("step")
        verbose_name_plural = _("Steps")

    def __str__(self):
        return f"{self.topic} · {self.order}. {self.title}"

    @property
    def paragraphs(self):
        return [p.strip() for p in self.body.split("\n\n") if p.strip()]

    @property
    def cards(self):
        result = []
        for line in self.body.splitlines():
            if "|" in line:
                front, back = line.split("|", 1)
                result.append({"front": front.strip(), "back": back.strip()})
        return result

    def interpret(self, score, max_score):
        share = score / max_score if max_score else 0
        if share < 0.4:
            return "low", self.result_low
        if share < 0.75:
            return "mid", self.result_mid
        return "high", self.result_high


class QuizQuestion(models.Model):
    step = models.ForeignKey(Step, verbose_name=_("step"), on_delete=models.CASCADE, related_name="questions")
    order = models.PositiveSmallIntegerField(_("order"), default=1)
    text = models.CharField(_("question"), max_length=300)
    options = models.TextField(
        _("answer options"),
        help_text=_(
            "One option per line as “answer | points”, e.g. “Often | 2”. "
            "In a situation game add feedback: “answer | points | feedback”."
        ),
    )

    class Meta:
        ordering = ["step", "order", "id"]
        verbose_name = _("test question")
        verbose_name_plural = _("test questions")

    def __str__(self):
        return self.text

    @property
    def option_list(self):
        result = []
        for i, line in enumerate(l for l in self.options.splitlines() if l.strip()):
            label, _sep, rest = line.partition("|")
            points, _sep, feedback = rest.partition("|")
            try:
                value = int(points.strip())
            except ValueError:
                value = 0
            result.append({"index": i, "label": label.strip(), "points": value, "feedback": feedback.strip()})
        return result

    @property
    def max_points(self):
        return max((o["points"] for o in self.option_list), default=0)


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("In progress")
        COMPLETED = "completed", _("Completed")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.ACTIVE)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("user", "topic")]
        ordering = ["-last_activity"]
        verbose_name = _("enrollment")
        verbose_name_plural = _("enrollments")

    def __str__(self):
        return f"{self.user} → {self.topic}"

    @property
    def completed_step_ids(self):
        return set(self.completions.values_list("step_id", flat=True))

    @property
    def progress_percent(self):
        total = self.topic.steps.count()
        if not total:
            return 0
        return round(100 * self.completions.count() / total)

    def next_step(self):
        done = self.completed_step_ids
        for step in self.topic.steps.all():
            if step.id not in done:
                return step
        return None

    @property
    def is_abandoned(self):
        cutoff = timezone.now() - timedelta(days=settings.ABANDON_AFTER_DAYS)
        return self.status == self.Status.ACTIVE and self.last_activity < cutoff

    def touch(self):
        self.last_activity = timezone.now()
        self.save(update_fields=["last_activity"])


class StepCompletion(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="completions")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="completions")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("enrollment", "step")]


class QuizResult(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="quiz_results")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="quiz_results")
    score = models.PositiveIntegerField(_("score"))
    max_score = models.PositiveIntegerField(_("maximum"))
    band = models.CharField(_("result"), max_length=10)
    answers = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("test result")
        verbose_name_plural = _("test results")

    @property
    def percent(self):
        return round(100 * self.score / self.max_score) if self.max_score else 0


class Reflection(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="reflections")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="reflections")
    text = models.TextField(_("answer"))
    ai_feedback = models.TextField(_("AI feedback"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("reflection")
        verbose_name_plural = _("reflections")


class Reminder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reminders")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="reminders")
    remind_at = models.DateTimeField(_("remind at"))
    note = models.CharField(_("note"), max_length=200, blank=True)
    is_done = models.BooleanField(_("done"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["remind_at"]
        verbose_name = _("reminder")
        verbose_name_plural = _("reminders")

    def __str__(self):
        return f"{self.topic} @ {self.remind_at:%Y-%m-%d %H:%M}"

    @property
    def is_due(self):
        return not self.is_done and self.remind_at <= timezone.now()
