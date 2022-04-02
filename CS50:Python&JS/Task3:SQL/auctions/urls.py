from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/<str:status>", views.page, name="page"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:cat>", views.sel_cat, name="sel_cat"),
    path("my", views.my, name="my"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("wonauctions", views.wonauctions, name="wonauctions"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
