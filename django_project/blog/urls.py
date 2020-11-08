from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/classroom/<int:id>', views.classroom, name='classroom'),
]
