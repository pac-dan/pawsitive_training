from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons_display, name='lessons'),
    path('<int:pk>/', views.lesson_detail, name='lesson_detail'),
]