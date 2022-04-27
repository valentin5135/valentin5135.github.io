
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("profile/<int:pk>", views.profile, name="profile"),

    path("posts", views.create_post, name="create_post"),
    path("posts/<int:post_id>", views.post, name="post"),

    path("likes/<int:post_id>", views.like, name="like"),

    path("follows/<int:profile_id>", views.follow, name="follow"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
