"""
URL Configuration for ecommerce_platform application.
This file routes all incoming requests to appropriate app handlers.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ============================================================================
# URL PATTERNS - Main application routes
# ============================================================================
urlpatterns = [
    # Admin panel URL
    path('admin/', admin.site.urls),
    
    # Products app URLs - catalog, search, product details
    path('', include('products.urls', namespace='products')),
    
    # Accounts app URLs - login, registration, user profile
    path('accounts/', include('accounts.urls', namespace='accounts')),
    
    # Cart app URLs - add, remove, view cart
    path('cart/', include('cart.urls', namespace='cart')),
    
    # Orders app URLs - order creation, history, tracking
    path('orders/', include('orders.urls', namespace='orders')),
]

# ============================================================================
# STATIC AND MEDIA FILES SERVING (Development only)
# ============================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
