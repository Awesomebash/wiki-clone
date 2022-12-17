from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("rnd/random", views.rnd, name="rnd"),
    path("crt/create", views.create, name="create"),
    path("edt/<str:title>", views.edit, name="edit"),
    path("<str:title>", views.entry, name="entry")
]
