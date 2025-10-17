from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('tools/', views.tool_list, name='tool_list'),
    path('tools/<slug:slug>/', views.tool_detail, name='tool_detail'),
    path('kategorie/<slug:slug>/', views.category_detail, name='category_detail'),
]
