from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from care.models import Connection, Message, MoodEntry
from learning.models import Enrollment, Reflection, Step, Topic

FETCH = {"HTTP_X_REQUESTED_WITH": "fetch"}


class CareTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("setup_roles", verbosity=0)
        call_command("seed_demo", verbosity=0)
        cls.psych = User.objects.get(username="gulnora.saidova")
        cls.client_user = User.objects.create_user("teen", password="Str0ng-pass!", first_name="Aziza", age_group="teens")
        cls.stranger = User.objects.create_user("stranger", password="Str0ng-pass!")

    def choose(self, concern="Imtihondan qo‘rqaman"):
        self.client.force_login(self.client_user)
        return self.client.post(reverse("care:choose", args=[self.psych.username]), {"concern": concern})

    def test_directory_filters_by_age_and_language(self):
        r = self.client.get(reverse("care:psychologists"), {"age": "children"})
        self.assertEqual([p.username for p in r.context["psychologists"]], ["gulnora.saidova"])
        r = self.client.get(reverse("care:psychologists"), {"age": "seniors"})
        self.assertEqual([p.username for p in r.context["psychologists"]], ["aziz.rahimov"])
        r = self.client.get(reverse("care:psychologists"), {"lang": "en"})
        self.assertEqual([p.username for p in r.context["psychologists"]], ["dilnoza.karimova"])
        # Logged-in clients see psychologists for their own age group by default.
        self.client.force_login(self.client_user)
        r = self.client.get(reverse("care:psychologists"))
        self.assertEqual(r.context["active_age"], "teens")
        self.assertEqual(self.client.get(reverse("care:psychologist", args=[self.psych.username])).status_code, 200)

    def test_demo_psychologists_can_open_studio(self):
        self.assertTrue(self.psych.is_staff)
        self.client.force_login(self.psych)
        self.assertEqual(self.client.get(reverse("admin:learning_topic_changelist")).status_code, 200)

    def test_any_age_filter_overrides_default(self):
        self.client.force_login(self.client_user)
        r = self.client.get(reverse("care:psychologists"), {"age": ""})
        self.assertEqual(r.context["active_age"], "")
        self.assertEqual(len(r.context["psychologists"]), 3)

    def test_studio_hides_topic_filters_from_psychologists(self):
        self.client.force_login(self.psych)
        r = self.client.get(reverse("admin:learning_step_changelist"))
        self.assertEqual([f.field_path for f in r.context["cl"].filter_specs], ["kind"])

    def test_psychologist_creates_topic_in_studio(self):
        from learning.models import Category

        self.client.force_login(self.psych)
        data = {
            "title_uz": "Yangi mavzu", "summary_uz": "Qisqa", "category": Category.objects.first().pk,
            "icon": "🌟", "color": "violet", "level": "beginner", "duration_minutes": 10, "is_published": "on",
            "steps-TOTAL_FORMS": "1", "steps-INITIAL_FORMS": "0", "steps-MIN_NUM_FORMS": "0", "steps-MAX_NUM_FORMS": "1000",
            "steps-0-order": "1", "steps-0-kind": "lesson", "steps-0-title_uz": "Kirish",
        }
        r = self.client.post(reverse("admin:learning_topic_add"), data)
        self.assertEqual(r.status_code, 302, r.content[:3000])
        topic = Topic.objects.get(title_uz="Yangi mavzu")
        self.assertEqual(topic.author, self.psych)
        self.assertEqual(topic.steps.count(), 1)
        # Duplicate step numbers are rejected by the form instead of crashing.
        data.update({"title_uz": "Ikkinchi", "steps-TOTAL_FORMS": "2", "steps-1-order": "1", "steps-1-kind": "lesson", "steps-1-title_uz": "Takror"})
        r = self.client.post(reverse("admin:learning_topic_add"), data)
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Topic.objects.filter(title_uz="Ikkinchi").exists())

    def test_unverified_psychologist_is_hidden(self):
        User.objects.create_user("newbie", password="x", role=User.Role.PSYCHOLOGIST)
        self.assertEqual(self.client.get(reverse("care:psychologist", args=["newbie"])).status_code, 404)

    def test_choose_accept_chat_flow(self):
        r = self.choose()
        connection = Connection.objects.get()
        self.assertRedirects(r, reverse("care:chat", args=[connection.pk]))
        self.assertEqual(connection.status, Connection.Status.PENDING)
        self.assertEqual(connection.messages.count(), 1)
        # Choosing again reuses the open conversation.
        self.choose()
        self.assertEqual(Connection.objects.count(), 1)

        # Psychologist sees the request, but no progress until accepting.
        self.client.force_login(self.psych)
        dash = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(len(dash.context["requests"]), 1)
        chat = self.client.get(reverse("care:chat", args=[connection.pk]))
        self.assertNotIn("client_enrollments", chat.context)
        self.client.post(reverse("care:respond", args=[connection.pk]), {"action": "accept"})
        connection.refresh_from_db()
        self.assertEqual(connection.status, Connection.Status.ACTIVE)
        chat = self.client.get(reverse("care:chat", args=[connection.pk]))
        self.assertIn("client_enrollments", chat.context)

        # Psychologist recommends a topic; client polls and sees it.
        topic = Topic.objects.get(slug="solving-conflicts")
        r = self.client.post(reverse("care:send", args=[connection.pk]), {"text": "", "topic": topic.pk}, **FETCH)
        self.assertEqual(r.status_code, 200)
        self.assertIn(topic.title_uz, r.json()["html"])
        self.client.force_login(self.client_user)
        before = Message.objects.filter(connection=connection).order_by("pk").first().pk
        data = self.client.get(reverse("care:poll", args=[connection.pk]), {"after": before}).json()
        self.assertIn("msg-topic", data["html"])
        self.assertEqual(data["status"], "active")
        self.assertFalse(Message.objects.filter(connection=connection, read_at__isnull=True).exclude(sender=self.client_user).exists())

        # Client replies; psychologist gets an unread badge.
        self.client.post(reverse("care:send", args=[connection.pk]), {"text": "Rahmat!"}, **FETCH)
        self.client.force_login(self.psych)
        self.assertEqual(self.client.get(reverse("care:inbox")).context["unread_messages_count"], 1)

        # Closing the conversation blocks new messages.
        self.client.post(reverse("care:respond", args=[connection.pk]), {"action": "end"})
        self.assertEqual(self.client.post(reverse("care:send", args=[connection.pk]), {"text": "hi"}).status_code, 403)

    def test_bad_topic_id_is_ignored(self):
        self.choose()
        connection = Connection.objects.get()
        self.client.force_login(self.psych)
        r = self.client.post(reverse("care:send", args=[connection.pk]), {"text": "hi", "topic": "abc"}, **FETCH)
        self.assertEqual(r.status_code, 200)

    def test_extreme_calendar_month_does_not_crash(self):
        self.client.force_login(self.client_user)
        for value in ("1-1", "9999-12", "2026-13", "x"):
            self.assertEqual(self.client.get(reverse("accounts:dashboard"), {"month": value}).status_code, 200)

    def test_healthz_ignores_unknown_host(self):
        self.assertEqual(self.client.get("/healthz", HTTP_HOST="10.0.0.5:10000").status_code, 200)

    def test_clients_cannot_send_topics_or_accept(self):
        self.choose()
        connection = Connection.objects.get()
        topic = Topic.objects.first()
        self.client.post(reverse("care:send", args=[connection.pk]), {"text": "x", "topic": topic.pk})
        self.assertFalse(Message.objects.filter(topic__isnull=False).exists())
        self.assertEqual(self.client.post(reverse("care:respond", args=[connection.pk]), {"action": "accept"}).status_code, 404)

    def test_chat_is_private(self):
        self.choose()
        connection = Connection.objects.get()
        self.client.force_login(self.stranger)
        for name in ("care:chat", "care:poll"):
            self.assertEqual(self.client.get(reverse(name, args=[connection.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("care:send", args=[connection.pk]), {"text": "spy"}).status_code, 404)

    def test_psychologist_cannot_choose_psychologist(self):
        self.client.force_login(User.objects.get(username="aziz.rahimov"))
        self.client.post(reverse("care:choose", args=[self.psych.username]))
        self.assertFalse(Connection.objects.exists())

    def test_not_accepting_clients(self):
        User.objects.filter(pk=self.psych.pk).update(accepts_clients=False)
        self.choose()
        self.assertFalse(Connection.objects.exists())

    def test_mood_checkin_updates_today(self):
        self.client.force_login(self.client_user)
        self.assertEqual(self.client.post(reverse("care:mood"), {"mood": 4}, **FETCH).json()["emoji"], "🙂")
        self.client.post(reverse("care:mood"), {"mood": 2}, **FETCH)
        self.assertEqual(MoodEntry.objects.get(user=self.client_user).mood, 2)
        self.assertEqual(self.client.post(reverse("care:mood"), {"mood": 9}, **FETCH).status_code, 400)
        dash = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(dash.context["today_mood"].mood, 2)
        self.assertEqual(len(dash.context["moods"]), 14)


class PracticeAndGameTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)
        cls.user = User.objects.create_user("player", password="Str0ng-pass!")

    def test_practice_hub_lists_tests_and_games(self):
        r = self.client.get(reverse("core:practice"))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(all(s.kind == "quiz" for s in r.context["tests"]))
        self.assertIn("scenario", {s.kind for s in r.context["games"]})

    def test_situation_game(self):
        self.client.force_login(self.user)
        topic = Topic.objects.get(slug="solving-conflicts")
        step = topic.steps.get(kind=Step.Kind.SCENARIO)
        options = step.questions.first().option_list
        self.assertEqual(options[1]["points"], 2)
        self.assertTrue(options[1]["feedback"])
        r = self.client.get(reverse("learning:step", args=[topic.slug, step.order]))
        self.assertContains(r, "data-scenario")
        self.client.post(reverse("learning:step_submit", args=[topic.slug, step.order]))
        self.assertIn(step.id, Enrollment.objects.get(user=self.user, topic=topic).completed_step_ids)

    def test_continue_goes_to_step_after_current(self):
        self.client.force_login(self.user)
        topic = Topic.objects.get(slug="solving-conflicts")
        game = topic.steps.get(kind=Step.Kind.SCENARIO)
        r = self.client.post(reverse("learning:step_submit", args=[topic.slug, game.order]))
        nxt = topic.steps.filter(order__gt=game.order).first()
        self.assertRedirects(r, reverse("learning:step", args=[topic.slug, nxt.order]))
        r = self.client.get(reverse("learning:continue", args=[topic.slug]), {"after": game.order})
        self.assertRedirects(r, reverse("learning:step", args=[topic.slug, nxt.order]))

    def test_step_numbers_are_unique_per_topic(self):
        from django.db import IntegrityError, transaction

        topic = Topic.objects.first()
        with self.assertRaises(IntegrityError), transaction.atomic():
            Step.objects.create(topic=topic, order=topic.steps.first().order, title_uz="Takror")

    def test_pause_rejects_external_redirect(self):
        self.client.force_login(self.user)
        topic = Topic.objects.first()
        past = (timezone.localtime() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")
        r = self.client.post(reverse("learning:pause", args=[topic.slug]), {"remind_at": past, "next": "https://evil.example/"})
        self.assertEqual(r["Location"], topic.get_absolute_url())

    @override_settings(OPENROUTER_API_KEY="k", AI_DAILY_LIMIT=1)
    def test_ai_daily_limit(self):
        from unittest import mock

        self.client.force_login(self.user)
        topic = Topic.objects.get(slug="know-yourself")
        step = topic.steps.get(kind="reflection")
        fake = mock.Mock()
        fake.json.return_value = {"choices": [{"message": {"content": "Zo‘r!"}}]}
        with mock.patch("learning.ai.requests.post", return_value=fake) as post:
            url = reverse("learning:step_submit", args=[topic.slug, step.order])
            self.client.post(url, {"text": "Birinchi javob", "ai": "1"})
            self.client.post(url, {"text": "Ikkinchi javob", "ai": "1"})
        self.assertEqual(post.call_count, 1)
        self.assertEqual(Reflection.objects.exclude(ai_feedback="").count(), 1)
