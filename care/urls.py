from django.urls import path

from . import views

app_name = "care"

urlpatterns = [
    path("psychologists/", views.psychologist_list, name="psychologists"),
    path("psychologists/<str:username>/", views.psychologist_detail, name="psychologist"),
    path("psychologists/<str:username>/choose/", views.choose, name="choose"),
    path("chat/", views.inbox, name="inbox"),
    path("chat/<int:pk>/", views.chat, name="chat"),
    path("chat/<int:pk>/send/", views.send, name="send"),
    path("chat/<int:pk>/poll/", views.poll, name="poll"),
    path("chat/<int:pk>/respond/", views.respond, name="respond"),
    path("mood/", views.mood, name="mood"),
]
