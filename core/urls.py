from django.urls import path

from learning import views as learning_views

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("practice/", learning_views.practice, name="practice"),
    path("healthz", views.healthz, name="healthz"),
]
