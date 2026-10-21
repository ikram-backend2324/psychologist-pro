from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render

from accounts.models import User
from care.views import verified_psychologists
from learning.models import Category, Enrollment, Topic


def home(request):
    topics = (
        Topic.objects.published()
        .select_related("category", "author")
        .annotate(step_count=Count("steps", distinct=True), learner_count=Count("enrollments", distinct=True))[:6]
    )
    return render(
        request,
        "core/home.html",
        {
            "topics": topics,
            "categories": Category.objects.annotate(n=Count("topics", filter=Q(topics__is_published=True))),
            "psychologists": verified_psychologists().order_by("-topic_count", "first_name")[:4],
            "counts": {
                "topics": Topic.objects.published().count(),
                "psychologists": User.objects.filter(role=User.Role.PSYCHOLOGIST, is_verified=True).count(),
                "learners": User.objects.filter(role=User.Role.CLIENT).count(),
                "completed": Enrollment.objects.filter(status=Enrollment.Status.COMPLETED).count(),
            },
        },
    )


def healthz(request):
    return JsonResponse({"status": "ok"})
