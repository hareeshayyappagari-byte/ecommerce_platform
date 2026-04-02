"""
Admin configuration for accounts app.
Customizes Django admin interface for managing user accounts and profiles.
"""

from django.contrib import admin
from .models import UserProfile, Address


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model"""
    list_display = ['user', 'phone_number', 'account_type', 'is_newsletter_subscribed']
    list_filter = ['account_type', 'is_newsletter_subscribed', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin interface for Address model"""
    list_display = ['full_name', 'user', 'address_type', 'city', 'country', 'is_default']
    list_filter = ['address_type', 'country', 'is_default']
    search_fields = ['full_name', 'user__username', 'city', 'country']
    readonly_fields = ['created_at', 'updated_at']
