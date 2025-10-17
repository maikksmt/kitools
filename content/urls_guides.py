from django.urls import path
from . import views_guides

app_name = 'guides'

urlpatterns = [
    path('', views_guides.index, name='index'),
    path('<slug:slug>/', views_guides.detail, name='detail'),
]
