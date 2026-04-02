"""
URL configuration for accounts app.
Defines routes for user registration, login, profile, and address management.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication routes
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Profile routes
    path('profile/', views.user_profile, name='profile'),
    
    # Address management routes
    path('addresses/', views.user_addresses, name='addresses'),
    path('address/add/', views.add_address, name='add-address'),
    path('address/<int:address_id>/edit/', views.edit_address, name='edit-address'),
    path('address/<int:address_id>/delete/', views.delete_address, name='delete-address'),
    path('address/<int:address_id>/set-default/', views.set_default_address, name='set-default-address'),
]
