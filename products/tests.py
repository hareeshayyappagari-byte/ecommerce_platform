"""
Tests for products app.
Contains unit tests and integration tests for product functionality.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Category, Product, Review


class CategoryModelTest(TestCase):
    """Test cases for Category model"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic products",
            slug="electronics"
        )
    
    def test_category_creation(self):
        """Test category can be created with correct data"""
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.slug, "electronics")
    
    def test_category_string_representation(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), "Electronics")


class ProductModelTest(TestCase):
    """Test cases for Product model"""
    
    def setUp(self):
        """Set up test data"""
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
    
    def test_product_creation(self):
        """Test product can be created"""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.sku, "TEST-001")
    
    def test_product_is_in_stock(self):
        """Test product stock checking"""
        self.assertTrue(self.product.is_in_stock())
    
    def test_product_discount_percentage(self):
        """Test discount percentage calculation"""
        self.product.discount_price = 79.99
        discount = self.product.get_discount_percentage()
        self.assertGreater(discount, 0)


class ReviewModelTest(TestCase):
    """Test cases for Review model"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            sku="TEST-001",
            category=self.category,
            price=99.99
        )
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="Great Product",
            content="This product is amazing!"
        )
    
    def test_review_creation(self):
        """Test review can be created"""
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.title, "Great Product")
    
    def test_review_string_representation(self):
        """Test review string representation"""
        review_str = str(self.review)
        self.assertIn("testuser", review_str)
        self.assertIn("5★", review_str)
