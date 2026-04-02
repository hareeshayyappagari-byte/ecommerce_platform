"""
Tests for orders app.
Contains unit tests for order management functionality.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Category, Product
from accounts.models import Address
from orders.models import Order, OrderItem
from decimal import Decimal


class OrderModelTest(TestCase):
    """Test cases for Order model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.address = Address.objects.create(
            user=self.user,
            address_type="shipping",
            full_name="John Doe",
            street_address_line_1="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
            phone_number="+1234567890"
        )
        
        self.order = Order.objects.create(
            order_number="ORD-20240101-ABC12345",
            customer=self.user,
            shipping_address=self.address,
            status="confirmed",
            total_amount=Decimal("199.99")
        )
    
    def test_order_creation(self):
        """Test order can be created"""
        self.assertEqual(self.order.customer, self.user)
        self.assertEqual(self.order.status, "confirmed")
    
    def test_order_total_calculation(self):
        """Test order total is calculated correctly"""
        self.assertEqual(self.order.total_amount, Decimal("199.99"))


class OrderItemTest(TestCase):
    """Test cases for OrderItem model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.address = Address.objects.create(
            user=self.user,
            address_type="shipping",
            full_name="John Doe",
            street_address_line_1="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
            phone_number="+1234567890"
        )
        
        self.order = Order.objects.create(
            order_number="ORD-20240101-ABC12345",
            customer=self.user,
            shipping_address=self.address,
            status="confirmed",
            total_amount=Decimal("199.99")
        )
        
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
        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name="Test Product",
            product_price=Decimal("99.99"),
            product_sku="TEST-001",
            quantity=2
        )
    
    def test_order_item_creation(self):
        """Test order item can be created"""
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.product_name, "Test Product")
    
    def test_order_item_total(self):
        """Test order item total calculation"""
        total = self.order_item.get_item_total()
        expected = Decimal("99.99") * 2
        self.assertEqual(total, expected)
