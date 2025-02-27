from django.urls import path
from . import views

urlpatterns = [
    path('', views.training_display, name='training'),
    path('<int:pk>/', views.training_detail, name='training_detail'),
]