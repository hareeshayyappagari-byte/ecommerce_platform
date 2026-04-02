"""
Database models for products app.
Defines Product, Category, Review, and Inventory models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Category(models.Model):
    """
    Product Category model.
    Stores product categories for organized catalog navigation.
    """
    # Category name - unique identifier for category
    name = models.CharField(max_length=100, unique=True, db_index=True)
    
    # Category description - provides information about category
    description = models.TextField(blank=True, null=True)
    
    # Slug - URL-friendly version of category name
    slug = models.SlugField(unique=True, db_index=True)
    
    # Timestamps - track creation and modification dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Model metadata configuration"""
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        """String representation of category"""
        return self.name


class Product(models.Model):
    """
    Product model.
    Represents individual products available in the e-commerce store.
    """
    # Product name - title of the product
    name = models.CharField(max_length=200, db_index=True)
    
    # Product description - detailed information about product
    description = models.TextField()
    
    # Product SKU - Stock Keeping Unit for inventory tracking
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    
    # Category - foreign key link to Category model
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    
    # Price - product selling price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Discount price - optional discounted price
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Product image - visual representation
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Stock quantity - number of items in inventory
    stock_quantity = models.IntegerField(default=0)
    
    # Is featured - flag to highlight featured products on homepage
    is_featured = models.BooleanField(default=False)
    
    # Is active - flag to enable/disable product listing
    is_active = models.BooleanField(default=True)
    
    # Timestamps - track creation and modification dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Model metadata configuration"""
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'is_active']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        """String representation of product"""
        return self.name
    
    def get_discount_percentage(self):
        """Calculate discount percentage if discount price exists"""
        if self.discount_price:
            discount = (self.price - self.discount_price) / self.price * 100
            return int(discount)
        return 0
    
    def is_in_stock(self):
        """Check if product is available in stock"""
        return self.stock_quantity > 0


class Review(models.Model):
    """
    Review model.
    Stores customer reviews and ratings for products.
    """
    # Product being reviewed - foreign key to Product
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    # User who wrote the review - foreign key to User
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_reviews'
    )
    
    # Rating - numeric rating from 1 to 5 stars
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Review title - short summary of review
    title = models.CharField(max_length=100)
    
    # Review content - detailed review text
    content = models.TextField()
    
    # Timestamps - track creation and modification dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Model metadata configuration"""
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # One review per user per product
    
    def __str__(self):
        """String representation of review"""
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"


class ProductImage(models.Model):
    """
    Product Image model.
    Stores multiple images for each product.
    """
    # Product - foreign key to Product model
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    
    # Image file
    image = models.ImageField(upload_to='products/')
    
    # Display order for multiple images
    order = models.IntegerField(default=0)
    
    # Timestamp - when image was uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Model metadata configuration"""
        ordering = ['order']
    
    def __str__(self):
        """String representation of product image"""
        return f"{self.product.name} - Image {self.order}"
