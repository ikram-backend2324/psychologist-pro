from django.urls import path

from . import views

app_name = "learning"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("reminders/<int:pk>/calendar.ics", views.reminder_ics, name="reminder_ics"),
    path("reminders/<int:pk>/google/", views.reminder_google, name="reminder_google"),
    path("reminders/<int:pk>/done/", views.reminder_done, name="reminder_done"),
    path("<slug:slug>/", views.topic_detail, name="topic"),
    path("<slug:slug>/start/", views.start, name="start"),
    path("<slug:slug>/continue/", views.continue_topic, name="continue"),
    path("<slug:slug>/pause/", views.pause, name="pause"),
    path("<slug:slug>/finish/", views.finish, name="finish"),
    path("<slug:slug>/step/<int:order>/", views.step_view, name="step"),
    path("<slug:slug>/step/<int:order>/submit/", views.step_submit, name="step_submit"),
]
