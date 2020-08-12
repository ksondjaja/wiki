from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("create/preview", views.preview, name="preview"),
    path("create/save", views.save, name="save"),
    path("random", views.rand, name="random"),
    path("search", views.search, name="search"),
    path("wiki/<str:page>", views.entry, name="entry"),
    path("edit/<str:page>", views.edit, name="edit"),
    path("edit/<str:page>/preview", views.prevedit, name="prevedit"),
    path("edit/<str:page>/saved", views.saveedit, name="saveedit")
]
