from django.urls import path
from . import views

app_name = "starter"

urlpatterns = [
    path("", views.StarterGuideView.as_view(), name="index"),
    path("intro/", views.StarterIntroView.as_view(), name="intro"),
]
