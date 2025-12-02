from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_display, name='products_display'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/update/<int:product_id>/', views.update_stock, name='update_stock'),
    path('create/', views.create_product, name='create_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
