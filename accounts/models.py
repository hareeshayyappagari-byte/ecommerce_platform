"""
Database models for accounts app.
Defines user profile and customer information models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Address(models.Model):
    """
    Address model.
    Stores address information for users (shipping, billing, etc).
    """
    # Address types
    ADDRESS_TYPES = [
        ('billing', 'Billing Address'),
        ('shipping', 'Shipping Address'),
        ('default', 'Default Address'),
    ]
    
    # User who owns the address
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    
    # Type of address
    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPES,
        default='default'
    )
    
    # Full name for address
    full_name = models.CharField(max_length=100)
    
    # Street address lines
    street_address_line_1 = models.CharField(max_length=255)
    street_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    
    # City
    city = models.CharField(max_length=100)
    
    # State or province
    state = models.CharField(max_length=100)
    
    # Postal code or ZIP code
    postal_code = models.CharField(max_length=20)
    
    # Country
    country = models.CharField(max_length=100)
    
    # Phone number
    phone_number = models.CharField(max_length=20)
    
    # Is default address flag
    is_default = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Model metadata configuration"""
        verbose_name_plural = "Addresses"
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        """String representation of address"""
        return f"{self.full_name} - {self.city}, {self.state}"


class UserProfile(models.Model):
    """
    Extended User Profile model.
    Stores additional user information beyond Django's default User model.
    """
    # One-to-one relationship with Django User model
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Phone number
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Date of birth
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Profile picture
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        default=None
    )
    
    # Bio or about information
    bio = models.TextField(blank=True, null=True, max_length=500)
    
    # Account type - individual or business
    ACCOUNT_TYPES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
    ]
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
        default='individual'
    )
    
    # Newsletter subscription flag
    is_newsletter_subscribed = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Model metadata configuration"""
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        """String representation of user profile"""
        return f"{self.user.get_full_name() or self.user.username} Profile"


# ============================================================================
# SIGNAL HANDLERS - Automatic profile creation
# ============================================================================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create UserProfile when User is created.
    Automatically creates a profile for new user accounts.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save UserProfile when User is saved.
    Ensures profile is saved when user data is updated.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
