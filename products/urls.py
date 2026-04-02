"""
URL configuration for products app.
Defines routes for product listing, search, and details.
"""

from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Homepage - product listing
    path('', views.ProductListView.as_view(), name='home'),
    
    # Product detail page
    path('product/<str:sku>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Add or edit product review
    path('product/<str:sku>/review/', views.add_review, name='add-review'),
    
    # Category-based product listing
    path('category/<slug:slug>/', views.category_products, name='category'),
    
    # Product search
    path('search/', views.search_products, name='search'),
]
