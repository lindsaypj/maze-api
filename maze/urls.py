from django.urls import path

from . import views

urlpatterns = [
  path("<int:width>x<int:height>/", views.MazeView.as_view(), name="MazeView"),
]