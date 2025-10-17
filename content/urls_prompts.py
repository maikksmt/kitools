from django.urls import path
from . import views_prompts as views

app_name = 'prompts'

urlpatterns = [
    path('', views.prompt_list, name='list'),
    path('<slug:slug>/', views.prompt_detail, name='detail'),
]
