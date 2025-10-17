from django.urls import path
from . import views_guides as views

app_name = 'guides'

urlpatterns = [
    path('', views.guide_list, name='list'),
    path('<slug:slug>/', views.guide_detail, name='detail'),
]
