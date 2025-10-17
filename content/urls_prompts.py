from django.urls import path
from . import views_prompts

app_name = 'prompts'

urlpatterns = [
    path('', views_prompts.index, name='index'),
    path('<slug:slug>/', views_prompts.detail, name='detail'),
]
