"""
Database models for orders app.
Defines Order and OrderItem models for managing customer orders.
"""

from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from accounts.models import Address
from decimal import Decimal


class Order(models.Model):
    """
    Order model.
    Represents a completed customer order.
    """
    # Order status choices
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Payment status choices
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Order number - unique identifier
    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Customer who placed the order
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    # Shipping address
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders_shipped'
    )
    
    # Billing address
    billing_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders_billed'
    )
    
    # Order status
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending'
    )
    
    # Payment status
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    
    # Payment method
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
        ('cod', 'Cash on Delivery'),
    ]
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cod'
    )
    
    # Subtotal - sum of product prices
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Shipping cost
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Tax amount
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Discount amount
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Total amount - final price to be paid
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Coupon code used (if any)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    
    # Special notes or instructions
    notes = models.TextField(blank=True, null=True)
    
    # Payment transaction ID
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        """Model metadata configuration"""
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['order_number']),
        ]
    
    def __str__(self):
        """String representation of order"""
        return f"Order {self.order_number}"
    
    def get_total_items(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.items.all())
    
    def calculate_total(self):
        """Recalculate and update total amount"""
        self.subtotal = sum(item.get_item_total() for item in self.items.all())
        self.total_amount = self.subtotal + self.shipping_cost + self.tax - self.discount
        return self.total_amount


class OrderItem(models.Model):
    """
    Order Item model.
    Represents individual products in an order.
    """
    # Order that contains this item
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    # Product being ordered
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    
    # Product details captured at time of order
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_sku = models.CharField(max_length=100)
    
    # Quantity ordered
    quantity = models.PositiveIntegerField()
    
    # Discount on this item (if any)
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Model metadata configuration"""
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        """String representation of order item"""
        return f"{self.product_name} x {self.quantity}"
    
    def get_item_total(self):
        """Calculate total for this order item"""
        return (self.product_price * self.quantity) - self.discount_amount


class OrderTracking(models.Model):
    """
    Order Tracking model.
    Stores tracking history and status updates for orders.
    """
    # Order being tracked
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='tracking_updates'
    )
    
    # Status of this update
    status = models.CharField(max_length=50)
    
    # Description of status update
    description = models.TextField()
    
    # Location where order is
    location = models.CharField(max_length=200, blank=True, null=True)
    
    # Tracking timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Model metadata configuration"""
        ordering = ['-timestamp']
        verbose_name_plural = "Order Tracking Updates"
    
    def __str__(self):
        """String representation of tracking update"""
        return f"{self.order.order_number} - {self.status}"
