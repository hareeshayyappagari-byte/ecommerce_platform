"""
Admin configuration for orders app.
Customizes Django admin interface for managing orders.
"""

from django.contrib import admin
from .models import Order, OrderItem, OrderTracking


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem within Order admin"""
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'product_sku', 'created_at']


class OrderTrackingInline(admin.TabularInline):
    """Inline admin for OrderTracking within Order admin"""
    model = OrderTracking
    extra = 1
    readonly_fields = ['timestamp']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model"""
    list_display = ['order_number', 'customer', 'status', 'payment_status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'customer__username', 'customer__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'get_total_items']
    inlines = [OrderItemInline, OrderTrackingInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'created_at', 'updated_at')
        }),
        ('Addresses', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('Order Status', {
            'fields': ('status', 'payment_status', 'shipped_at', 'delivered_at')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'transaction_id', 'coupon_code')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total_amount')
        }),
        ('Additional', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_total_items(self, obj):
        """Display total items in order"""
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'
    
    list_per_page = 20


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model"""
    list_display = ['order', 'product_name', 'quantity', 'product_price', 'get_item_total']
    list_filter = ['order__created_at', 'product__category']
    search_fields = ['order__order_number', 'product_name']
    readonly_fields = ['created_at']
    
    def get_item_total(self, obj):
        """Display total for each order item"""
        return f'${obj.get_item_total()}'
    get_item_total.short_description = 'Total'


@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    """Admin interface for OrderTracking model"""
    list_display = ['order', 'status', 'location', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['order__order_number', 'status']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
