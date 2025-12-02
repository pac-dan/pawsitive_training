from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.training_display, name='training_display'),
    path('search/', views.search, name='search'),
    path('category/<slug:category_slug>/', views.category_trainings,
         name='category_trainings'),
    path('manage/', views.training_list, name='training_list'),
    path('create/', views.create_training, name='create_training'),
    path('edit/<int:training_id>/', views.edit_training, name='edit_training'),
    path('delete/<int:training_id>/', views.delete_training,
         name='delete_training'),
    path('<int:pk>/', views.training_detail, name='training_detail'),
]
