from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.profile_dashboard, name='dashboard'),
    path('edit/', views.edit_profile, name='edit_profile'),
]