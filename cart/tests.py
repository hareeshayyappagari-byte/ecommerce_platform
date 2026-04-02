"""
Tests for cart app.
Contains unit tests for shopping cart functionality.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Category, Product
from cart.models import Cart, CartItem


class CartModelTest(TestCase):
    """Test cases for Cart model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.cart = Cart.objects.create(user=self.user)
    
    def test_cart_creation(self):
        """Test cart can be created for user"""
        self.assertEqual(self.cart.user, self.user)
    
    def test_cart_empty_check(self):
        """Test empty cart detection"""
        self.assertTrue(self.cart.is_empty())


class CartItemTest(TestCase):
    """Test cases for CartItem model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.cart = Cart.objects.create(user=self.user)
        
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            sku="TEST-001",
            category=self.category,
            price=99.99,
            stock_quantity=10
        )
        
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
    
    def test_cart_item_creation(self):
        """Test cart item can be added"""
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.product, self.product)
    
    def test_cart_item_total(self):
        """Test cart item total calculation"""
        total = self.cart_item.get_item_total()
        expected = 99.99 * 2
        self.assertEqual(total, expected)
