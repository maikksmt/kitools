from django.urls import path
from . import views_usecases

app_name = 'usecases'

urlpatterns = [
    path('<slug:slug>/', views_usecases.detail, name='detail'),
]
