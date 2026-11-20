"""Create or refresh the emotional intelligence course (8 topics, 4 languages).

Safe to run repeatedly: existing topics are left alone unless --refresh is given.
    python manage.py seed_ei            # create missing topics
    python manage.py seed_ei --refresh  # also rewrite texts of existing course topics
    python manage.py seed_ei --author some.username   # assign new topics to this psychologist
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import User
from learning.ei_content import EI_AUTHOR, EI_CATEGORY, EI_TOPICS
from learning.models import Category, QuizQuestion, Step, Topic

LANGS = ("uz", "kaa", "ru", "en")
EMPTY = ("", "", "", "")


def tr(obj, field, values):
    """values: (uz, kaa, ru, en); the untranslated base field gets the Uzbek text."""
    for lang, value in zip(LANGS, values):
        setattr(obj, f"{field}_{lang}", value)
    setattr(obj, field, values[0])


class Command(BaseCommand):
    help = "Create the 8-topic emotional intelligence course (safe to run repeatedly)."

    def add_arguments(self, parser):
        parser.add_argument("--refresh", action="store_true", help="Rewrite the texts of course topics that already exist.")
        parser.add_argument("--author", help="Username of the psychologist who owns new course topics (default: farida).")

    def get_author(self, username):
        from django.contrib.auth.models import Group

        from accounts.admin import PSYCHOLOGIST_GROUP

        if username:
            user = User.objects.filter(username=username).first()
            if user is None:
                raise CommandError(f"User “{username}” does not exist.")
            return user
        data = dict(EI_AUTHOR)
        user, created = User.objects.get_or_create(
            username=data.pop("username"),
            defaults=data | {"role": User.Role.PSYCHOLOGIST, "is_verified": True, "is_staff": True},
        )
        if created:
            user.set_unusable_password()  # an admin sets a password in the admin panel
            user.save()
            group = Group.objects.filter(name=PSYCHOLOGIST_GROUP).first()
            if group:
                user.groups.add(group)
        return user

    @transaction.atomic
    def handle(self, *args, **options):
        slug, icon, color, names = EI_CATEGORY
        category = Category.objects.filter(slug=slug).first() or Category(slug=slug, order=Category.objects.count())
        category.icon, category.color = icon, color
        tr(category, "name", names)
        category.save()

        author = None
        created = refreshed = skipped = 0
        for data in EI_TOPICS:
            topic = Topic.objects.filter(slug=data["slug"]).first()
            if topic and not options["refresh"]:
                skipped += 1
                continue
            if topic is None:
                author = author or self.get_author(options.get("author"))
                topic = Topic(slug=data["slug"], author=author, is_published=True)
                created += 1
            else:
                refreshed += 1
            topic.category = category
            topic.order = data["order"]
            topic.icon, topic.color, topic.level = data["icon"], data["color"], data["level"]
            topic.duration_minutes, topic.tags, topic.sources = data["minutes"], data["tags"], data["sources"]
            for field in ("title", "summary", "goal", "description"):
                tr(topic, field, data[field])
            topic.save()

            for order, s in enumerate(data["steps"], start=1):
                step = topic.steps.filter(order=order).first() or Step(topic=topic, order=order)
                step.kind = s["kind"]
                tr(step, "title", s["title"])
                tr(step, "body", s.get("body", EMPTY))
                if "breathing" in s:
                    step.inhale_seconds, step.hold_seconds, step.exhale_seconds, step.cycles = s["breathing"]
                for field, values in zip(("result_low", "result_mid", "result_high"), s.get("results", (EMPTY,) * 3)):
                    tr(step, field, values)
                step.save()
                questions = s.get("questions", [])
                for q_order, (text, options_text) in enumerate(questions, start=1):
                    question = step.questions.filter(order=q_order).first() or QuizQuestion(step=step, order=q_order)
                    tr(question, "text", text)
                    tr(question, "options", options_text)
                    question.save()
                step.questions.filter(order__gt=len(questions)).delete()
            # Steps beyond the course definition (only on refresh) are removed so the topic matches the guide.
            topic.steps.filter(order__gt=len(data["steps"])).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Emotional intelligence course ready: {created} new, {refreshed} refreshed, {skipped} unchanged topic(s)."
        ))
