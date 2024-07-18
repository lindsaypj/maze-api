from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:width>x<int:height>/", views.getMaze, name="getMaze"),
]