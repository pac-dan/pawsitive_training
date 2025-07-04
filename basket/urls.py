from django.urls import path
from . import views

urlpatterns = [
    path('', views.basket_detail, name='basket_detail'),
    path('add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('remove/<int:product_id>/', views.basket_remove, name='basket_remove'),
    path('update/<int:product_id>/', views.basket_update, name='basket_update'),
    path('info/<int:product_id>/', views.basket_info, name='basket_info'),
]