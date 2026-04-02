"""
Database models for cart app.
Defines Shopping Cart and Cart Item models for managing user shopping carts.
"""

from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal


class Cart(models.Model):
    """
    Shopping Cart model.
    Represents a shopping cart for each user session.
    """
    # User owner of the cart - anonymous users use session ID
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart'
    )
    
    # Session key for anonymous visitors
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Model metadata configuration"""
        verbose_name_plural = "Shopping Carts"
    
    def __str__(self):
        """String representation of cart"""
        if self.user:
            return f"Cart of {self.user.username}"
        return f"Anonymous Cart ({self.session_key})"
    
    def get_total_price(self):
        """Calculate total price of all items in cart"""
        total = sum(item.get_item_total() for item in self.items.all())
        return total
    
    def get_total_items_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    def is_empty(self):
        """Check if cart is empty"""
        return not self.items.exists()


class CartItem(models.Model):
    """
    Cart Item model.
    Represents individual products added to a shopping cart.
    """
    # Shopping cart that contains this item
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    # Product in the cart
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    
    # Quantity of product in cart
    quantity = models.PositiveIntegerField(default=1)
    
    # Timestamps
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Model metadata configuration"""
        unique_together = ['cart', 'product']  # One entry per product per cart
        verbose_name_plural = "Cart Items"
    
    def __str__(self):
        """String representation of cart item"""
        return f"{self.product.name} x {self.quantity}"
    
    def get_item_total(self):
        """Calculate total price for this cart item"""
        # Use discount price if available, otherwise use regular price
        price = self.product.discount_price or self.product.price
        return price * self.quantity
    
    def get_item_price(self):
        """Get the price per unit of this product"""
        return self.product.discount_price or self.product.price
