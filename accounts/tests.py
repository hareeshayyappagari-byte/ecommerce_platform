"""
Tests for accounts app.
Contains unit tests for user authentication and profile management.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile, Address


class UserProfileTest(TestCase):
    """Test cases for UserProfile model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_profile_created_on_user_creation(self):
        """Test profile is auto-created when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_profile_update(self):
        """Test profile can be updated"""
        profile = self.user.profile
        profile.phone_number = "+1234567890"
        profile.save()
        
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.phone_number, "+1234567890")


class AddressModelTest(TestCase):
    """Test cases for Address model"""
    
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
    
    def test_address_creation(self):
        """Test address can be created"""
        self.assertEqual(self.address.full_name, "John Doe")
        self.assertEqual(self.address.city, "New York")
    
    def test_address_string_representation(self):
        """Test address string representation"""
        address_str = str(self.address)
        self.assertIn("John Doe", address_str)
        self.assertIn("New York", address_str)
