"""
Admin configuration for cart app.
Customizes Django admin interface for managing shopping carts.
"""

from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for Cart model"""
    list_display = ['id', 'user', 'get_items_count', 'get_total_price', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'get_total_price']
    
    def get_items_count(self, obj):
        """Display count of items in cart"""
        return obj.get_total_items_count()
    get_items_count.short_description = 'Items'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for CartItem model"""
    list_display = ['cart', 'product', 'quantity', 'get_item_total', 'added_at']
    list_filter = ['added_at', 'product__category']
    search_fields = ['product__name', 'cart__user__username']
    readonly_fields = ['added_at', 'updated_at']
    
    def get_item_total(self, obj):
        """Display total price for cart item"""
        return f'${obj.get_item_total()}'
    get_item_total.short_description = 'Total'
