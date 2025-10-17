from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.tool_list, name='tool_list'),
    path('home/', views.home, name='home'),
    path('<slug:slug>/', views.tool_detail, name='tool_detail'),

]
