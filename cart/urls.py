"""
URL configuration for cart app.
Defines routes for shopping cart operations.
"""

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # View cart page
    path('', views.view_cart, name='view'),
    
    # Add product to cart
    path('add/<int:product_id>/', views.add_to_cart, name='add'),
    
    # Remove item from cart
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove'),
    
    # Update cart item quantity
    path('update/<int:item_id>/', views.update_cart_quantity, name='update'),
    
    # Clear entire cart
    path('clear/', views.clear_cart, name='clear'),
    
    # Get cart count via API
    path('count/', views.get_cart_count, name='count'),
]
