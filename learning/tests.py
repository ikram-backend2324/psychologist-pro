from datetime import timedelta
from unittest import mock

from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from learning.models import Enrollment, QuizResult, Reflection, Reminder, Topic

LANGS = ("uz", "kaa", "ru", "en")


class FlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("setup_roles", verbosity=0)
        call_command("seed_demo", verbosity=0)
        cls.topic = Topic.objects.get(slug="how-to-communicate-with-people")

    def register_client(self, username="ali"):
        r = self.client.post(
            reverse("accounts:register"),
            {"role": "client", "first_name": "Ali", "username": username, "password1": "Str0ng-pass!", "password2": "Str0ng-pass!"},
        )
        self.assertRedirects(r, reverse("accounts:dashboard"), fetch_redirect_response=False)
        return User.objects.get(username=username)

    def test_public_pages_in_every_language(self):
        urls = [reverse("core:home"), reverse("learning:catalog"), reverse("care:psychologists"), reverse("core:practice"),
                self.topic.get_absolute_url(), reverse("accounts:login"), reverse("accounts:register")]
        expected = {"uz": "Mavzular", "kaa": "Temalar", "ru": "Темы", "en": "Topics"}
        for lang in LANGS:
            self.client.post(reverse("set_language"), {"language": lang, "next": "/"})
            for url in urls:
                r = self.client.get(url)
                self.assertEqual(r.status_code, 200, f"{lang} {url}")
                self.assertContains(r, expected[lang])
        # Content translations follow the language too.
        self.client.post(reverse("set_language"), {"language": "kaa", "next": "/"})
        self.assertContains(self.client.get(self.topic.get_absolute_url()), "Adamlar menen qalay sóylesiw kerek")

    def test_catalog_filters(self):
        r = self.client.get(reverse("learning:catalog"), {"category": "stress"})
        self.assertEqual(len(r.context["topics"]), 1)
        r = self.client.get(reverse("learning:catalog"), {"q": "zzz-nothing"})
        self.assertEqual(len(r.context["topics"]), 0)

    def test_client_full_journey(self):
        user = self.register_client()
        r = self.client.post(reverse("learning:start", args=[self.topic.slug]))
        steps = list(self.topic.steps.all())
        self.assertRedirects(r, reverse("learning:step", args=[self.topic.slug, steps[0].order]))
        # Steps are not locked: tests and games can be opened directly (e.g. from the hub).
        self.assertEqual(self.client.get(reverse("learning:step", args=[self.topic.slug, steps[2].order])).status_code, 200)

        for step in steps:
            url = reverse("learning:step", args=[self.topic.slug, step.order])
            self.assertEqual(self.client.get(url).status_code, 200, step.kind)
            submit = reverse("learning:step_submit", args=[self.topic.slug, step.order])
            if step.kind == "quiz":
                answers = {f"q{q.id}": "2" for q in step.questions.all()}
                self.client.post(submit, answers)
                self.assertContains(self.client.get(url), "gauge")
            elif step.kind == "reflection":
                self.client.post(submit, {"text": "Men akam bilan bahslashdim."})
            else:
                self.client.post(submit)

        enrollment = Enrollment.objects.get(user=user, topic=self.topic)
        self.assertEqual(enrollment.status, Enrollment.Status.COMPLETED)
        self.assertEqual(enrollment.progress_percent, 100)
        result = QuizResult.objects.get(enrollment=enrollment)
        self.assertEqual((result.score, result.max_score), (6, 12))
        self.assertEqual(result.band, "mid")
        self.assertEqual(Reflection.objects.filter(enrollment=enrollment).count(), 1)
        self.assertEqual(self.client.get(reverse("learning:finish", args=[self.topic.slug])).status_code, 200)
        self.assertEqual(self.client.get(reverse("accounts:dashboard")).status_code, 200)

    def test_incomplete_quiz_is_rejected(self):
        self.register_client()
        self.client.post(reverse("learning:start", args=[self.topic.slug]))
        first = self.topic.steps.first()
        self.client.post(reverse("learning:step_submit", args=[self.topic.slug, first.order]))
        quiz = self.topic.steps.get(kind="quiz")
        self.client.post(reverse("learning:step_submit", args=[self.topic.slug, quiz.order]), {})
        self.assertFalse(QuizResult.objects.exists())

    def test_abandoned_topic_reminder_and_calendar(self):
        user = self.register_client()
        self.client.post(reverse("learning:start", args=[self.topic.slug]))
        Enrollment.objects.filter(user=user).update(last_activity=timezone.now() - timedelta(days=5))
        r = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(len(r.context["abandoned"]), 1)
        self.assertTrue(r.context["abandoned"][0].suggestions)

        when = timezone.localtime() + timedelta(days=1)
        r = self.client.post(reverse("learning:pause", args=[self.topic.slug]), {"remind_at": when.strftime("%Y-%m-%dT%H:%M")})
        self.assertRedirects(r, reverse("accounts:dashboard"), fetch_redirect_response=False)
        reminder = Reminder.objects.get(user=user)
        ics = self.client.get(reverse("learning:reminder_ics", args=[reminder.pk]))
        self.assertEqual(ics["Content-Type"], "text/calendar; charset=utf-8")
        self.assertIn(b"BEGIN:VEVENT", ics.content)
        google = self.client.get(reverse("learning:reminder_google", args=[reminder.pk]))
        self.assertTrue(google["Location"].startswith("https://calendar.google.com/"))

        # A due reminder shows a badge and the "come back" card.
        Reminder.objects.filter(pk=reminder.pk).update(remind_at=timezone.now() - timedelta(minutes=1))
        r = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(len(r.context["due_reminders"]), 1)
        self.assertEqual(r.context["due_reminders_count"], 1)
        # Past times are rejected.
        past = (timezone.localtime() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")
        self.client.post(reverse("learning:pause", args=[self.topic.slug]), {"remind_at": past})
        self.assertEqual(Reminder.objects.filter(user=user).count(), 1)

    def test_reminders_are_private(self):
        owner = self.register_client("owner")
        reminder = Reminder.objects.create(user=owner, topic=self.topic, remind_at=timezone.now() + timedelta(days=1))
        self.client.logout()
        self.register_client("other")
        self.assertEqual(self.client.get(reverse("learning:reminder_ics", args=[reminder.pk])).status_code, 404)

    @override_settings(OPENROUTER_API_KEY="test-key")
    def test_reflection_ai_feedback(self):
        self.register_client()
        reflection = self.topic.steps.get(kind="reflection")
        enrollment = Enrollment.objects.create(user=User.objects.get(username="ali"), topic=self.topic)
        for step in self.topic.steps.filter(order__lt=reflection.order):
            enrollment.completions.create(step=step)
        fake = mock.Mock()
        fake.json.return_value = {"choices": [{"message": {"content": "Ajoyib qadam!"}}]}
        fake.raise_for_status.return_value = None
        with mock.patch("learning.ai.requests.post", return_value=fake) as post:
            self.client.post(reverse("learning:step_submit", args=[self.topic.slug, reflection.order]), {"text": "Sinab ko‘raman", "ai": "1"})
        self.assertEqual(post.call_count, 1)
        self.assertEqual(Reflection.objects.get().ai_feedback, "Ajoyib qadam!")

    def test_psychologist_registration_and_studio(self):
        r = self.client.post(
            reverse("accounts:register"),
            {"role": "psychologist", "first_name": "Malika", "username": "malika", "specialization": "Oila psixologiyasi",
             "password1": "Str0ng-pass!", "password2": "Str0ng-pass!"},
        )
        self.assertEqual(r.status_code, 302)
        psych = User.objects.get(username="malika")
        self.assertFalse(psych.is_staff)
        self.assertEqual(self.client.get(reverse("accounts:dashboard")).status_code, 200)

        # Admin verifies via the bulk action.
        admin = User.objects.create_superuser("boss", password="Str0ng-pass!", role=User.Role.ADMIN)
        self.client.force_login(admin)
        self.client.post(reverse("admin:accounts_user_changelist"), {"action": "verify_psychologists", "_selected_action": [psych.pk]})
        psych.refresh_from_db()
        self.assertTrue(psych.is_verified and psych.is_staff)
        self.assertTrue(psych.groups.filter(name="Psychologists").exists())
        for name in ("admin:index", "admin:learning_topic_changelist", "admin:learning_step_changelist", "admin:accounts_user_changelist"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

        # The psychologist sees only their own topics in the studio.
        self.client.force_login(psych)
        r = self.client.get(reverse("admin:learning_topic_changelist"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context["cl"].result_count, 0)
        self.assertEqual(self.client.get(reverse("admin:learning_topic_add")).status_code, 200)
        foreign = Topic.objects.first()
        self.assertNotEqual(self.client.get(reverse("admin:learning_topic_change", args=[foreign.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin:accounts_user_changelist")).status_code, 403)

    def test_admin_login_page_for_anonymous_visitor(self):
        self.assertEqual(self.client.get(reverse("admin:login")).status_code, 200)

    def test_drafts_visible_only_to_author(self):
        Topic.objects.filter(pk=self.topic.pk).update(is_published=False)
        step = self.topic.steps.first()
        step_url = reverse("learning:step", args=[self.topic.slug, step.order])
        other_psych = User.objects.get(username="aziz.rahimov")
        other_psych.is_staff = True
        other_psych.save()
        self.client.force_login(other_psych)
        self.assertEqual(self.client.get(self.topic.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(step_url).status_code, 404)
        self.client.force_login(self.topic.author)
        self.assertEqual(self.client.get(self.topic.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(step_url).status_code, 200)

    def test_healthz(self):
        self.assertEqual(self.client.get("/healthz").json(), {"status": "ok"})
