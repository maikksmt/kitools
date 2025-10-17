from django.urls import path
from . import views_usecases as views

app_name = 'usecases'

urlpatterns = [
    path('', views.usecase_list, name='list'),
    path('<slug:slug>/', views.usecase_detail, name='detail'),
]
