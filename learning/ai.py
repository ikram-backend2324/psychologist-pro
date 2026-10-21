"""Optional OpenRouter-powered feedback on reflection answers.

Everything degrades gracefully: without OPENROUTER_API_KEY, or on any error, callers get None.
"""
import logging
from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone

from .models import Reflection

log = logging.getLogger(__name__)

LANGUAGE_NAMES = {"uz": "Uzbek (Latin script)", "kaa": "Karakalpak (Latin script)", "ru": "Russian", "en": "English"}

SYSTEM_PROMPT = (
    "You are a warm, careful assistant on a psychology self-help learning platform. "
    "A user answered a reflection question inside a topic prepared by a psychologist. "
    "Reply in {language} with 3-5 short sentences: acknowledge what they wrote, highlight one strength, "
    "and suggest one small, practical next step related to the topic. "
    "Do not diagnose, do not give medical advice, do not mention that you are an AI model. "
    "If the answer mentions self-harm, suicide or danger, gently urge them to contact local emergency "
    "services or a trusted person right now and to speak with a psychologist."
)


def is_enabled():
    return bool(settings.OPENROUTER_API_KEY)


def quota_left(user):
    """AI replies cost money, so each user gets a small daily allowance."""
    since = timezone.now() - timedelta(days=1)
    used = Reflection.objects.filter(enrollment__user=user, created_at__gte=since).exclude(ai_feedback="").count()
    return settings.AI_DAILY_LIMIT - used


def reflection_feedback(*, topic_title, question, answer, language):
    if not is_enabled():
        return None
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "HTTP-Referer": settings.SITE_URL,
                "X-Title": "Ruhiyat",
            },
            json={
                "model": settings.OPENROUTER_MODEL,
                "max_tokens": 350,
                "temperature": 0.6,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT.format(language=LANGUAGE_NAMES.get(language, "Uzbek"))},
                    {
                        "role": "user",
                        "content": f"Topic: {topic_title}\nQuestion: {question}\nUser's answer: {answer[:3000]}",
                    },
                ],
            },
            timeout=settings.AI_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip() or None
    except (requests.RequestException, KeyError, IndexError, ValueError):
        log.exception("OpenRouter reflection feedback failed")
        return None
