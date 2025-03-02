from django.urls import path
from . import views
from .views import training_display, search, training_detail, category_trainings

app_name = 'training'

urlpatterns = [
    path('', views.training_display, name='training_display'),
    path('<int:pk>/', views.training_detail, name='training_detail'),
    path('search/', search, name='search'),
    path('category/<slug:category_slug>/', category_trainings, name='category_trainings'),
]