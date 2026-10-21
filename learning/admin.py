from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline, TranslationTabularInline

from .models import Category, Enrollment, QuizQuestion, QuizResult, Reflection, Reminder, Step, Topic


def is_platform_admin(user):
    return user.is_superuser or getattr(user, "role", None) == "admin"


class OwnTopicsMixin:
    """Psychologists only see and edit content that belongs to their own topics."""

    topic_lookup = "topic__author"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if is_platform_admin(request.user):
            return qs
        return qs.filter(**{self.topic_lookup: request.user})

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "topic" and not is_platform_admin(request.user):
            kwargs["queryset"] = Topic.objects.filter(author=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("icon", "name", "slug", "color", "order", "topic_count")
    list_display_links = ("icon", "name")
    list_editable = ("order",)

    @admin.display(description=_("Topics"))
    def topic_count(self, obj):
        return obj.topics.count()


class StepInline(TranslationTabularInline):
    model = Step
    fields = ("order", "kind", "title")
    extra = 0
    show_change_link = True


@admin.register(Topic)
class TopicAdmin(OwnTopicsMixin, TranslationAdmin):
    topic_lookup = "author"
    list_display = ("badge", "title", "category", "author", "level", "steps_total", "learners", "is_published")
    list_display_links = ("badge", "title")
    list_filter = ("is_published", "category", "level")
    list_editable = ("is_published",)
    search_fields = ("title", "summary", "tags")
    inlines = [StepInline]
    fieldsets = (
        (_("Main"), {"fields": ("title", "summary", "goal", "description")}),
        (_("Look and placement"), {"fields": ("category", "author", "icon", "color", "level", "duration_minutes", "tags", "is_published", "slug")}),
    )
    readonly_fields = ()

    @admin.display(description="")
    def badge(self, obj):
        return format_html('<span style="font-size:1.4rem">{}</span>', obj.icon)

    @admin.display(description=_("Steps"))
    def steps_total(self, obj):
        return obj.steps.count()

    @admin.display(description=_("Learners"))
    def learners(self, obj):
        return obj.enrollments.count()

    def get_readonly_fields(self, request, obj=None):
        return ("author",) if not is_platform_admin(request.user) else ()

    def save_model(self, request, obj, form, change):
        if not is_platform_admin(request.user):
            obj.author = request.user
            if not request.user.is_verified:
                obj.is_published = False
        super().save_model(request, obj, form, change)


class QuizQuestionInline(TranslationStackedInline):
    model = QuizQuestion
    extra = 0
    fields = ("order", "text", "options")


@admin.register(Step)
class StepAdmin(OwnTopicsMixin, TranslationAdmin):
    list_display = ("topic", "order", "kind", "title")
    list_filter = ("kind", "topic")
    search_fields = ("title", "topic__title")
    inlines = [QuizQuestionInline]
    fieldsets = (
        (None, {"fields": ("topic", "order", "kind", "title", "body")}),
        (_("Breathing game"), {"fields": ("inhale_seconds", "hold_seconds", "exhale_seconds", "cycles")}),
        (_("Test results"), {"fields": ("result_low", "result_mid", "result_high")}),
    )


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Enrollment)
class EnrollmentAdmin(OwnTopicsMixin, ReadOnlyAdmin):
    list_display = ("user", "topic", "status", "progress", "started_at", "last_activity")
    list_filter = ("status", "topic")
    search_fields = ("user__username", "topic__title")

    @admin.display(description=_("Progress"))
    def progress(self, obj):
        return f"{obj.progress_percent}%"


@admin.register(QuizResult)
class QuizResultAdmin(OwnTopicsMixin, ReadOnlyAdmin):
    topic_lookup = "step__topic__author"
    list_display = ("student", "step", "score", "max_score", "band", "created_at")
    list_filter = ("band", "step__topic")

    @admin.display(description=_("Client"))
    def student(self, obj):
        return obj.enrollment.user


@admin.register(Reflection)
class ReflectionAdmin(OwnTopicsMixin, ReadOnlyAdmin):
    topic_lookup = "step__topic__author"
    list_display = ("student", "step", "short_text", "created_at")
    list_filter = ("step__topic",)

    @admin.display(description=_("Client"))
    def student(self, obj):
        return obj.enrollment.user

    @admin.display(description=_("Answer"))
    def short_text(self, obj):
        return obj.text[:80]


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "remind_at", "is_done")
    list_filter = ("is_done",)

    def has_module_permission(self, request):
        return is_platform_admin(request.user)
