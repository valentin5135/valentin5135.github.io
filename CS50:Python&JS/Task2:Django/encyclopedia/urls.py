from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("create", views.create, name="create"),
    path("randpage", views.randpage, name="randpage"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>/delete", views.delete, name="delete"),
    path("wiki/<str:title>/edit", views.edit, name="edit")

]
