from django.urls import path
from . import views
from .views import products_display, search, product_detail

app_name = 'products'

urlpatterns = [
    path('', views.products_display, name='products_display'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', search, name='search'),
]