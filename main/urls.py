from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("create", views.create, name="create"),
    path("join", views.join, name="join"),
    path("lobby/<int:id>", views.lobby, name="lobby")
]
