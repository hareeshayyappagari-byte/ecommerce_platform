"""
URL configuration for orders app.
Defines routes for order creation, history, tracking, and management.
"""

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Checkout and order creation
    path('checkout/', views.checkout, name='checkout'),
    
    # Order details
    path('<int:order_id>/', views.order_detail, name='order-detail'),
    
    # Order history
    path('history/', views.order_history, name='history'),
    
    # Track order
    path('<int:order_id>/track/', views.track_order, name='track'),
    
    # Cancel order
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel'),
]
