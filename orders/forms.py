"""
Django Forms for orders app.
Handles checkout and order-related forms.
"""

from django import forms
from accounts.models import Address


class CheckoutForm(forms.Form):
    """
    Checkout form.
    Collects shipping address, billing address, and payment information.
    """
    # Shipping address selection
    shipping_address = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        label='Shipping Address',
        empty_label=None,
    )
    
    # Billing address selection
    billing_address = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.RadioSelect,
        label='Billing Address (Optional)',
    )
    
    # Shipping method
    SHIPPING_CHOICES = [
        ('standard', 'Standard Shipping - 5-7 business days ($0)'),
        ('express', 'Express Shipping - 2-3 business days ($10)'),
        ('overnight', 'Overnight Shipping ($25)'),
    ]
    shipping_method = forms.ChoiceField(
        choices=SHIPPING_CHOICES,
        widget=forms.RadioSelect,
        initial='standard',
    )
    
    # Payment method
    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect,
        initial='cod',
    )
    
    # Coupon code
    coupon_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter coupon code (optional)',
        })
    )
    
    # Order notes
    notes = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Special instructions or notes for your order',
        })
    )
    
    # Agree to terms checkbox
    agree_to_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    
    def __init__(self, *args, user=None, **kwargs):
        """Initialize form with user's addresses"""
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter addresses for the user
            user_addresses = Address.objects.filter(user=user)
            self.fields['shipping_address'].queryset = user_addresses
            self.fields['billing_address'].queryset = user_addresses
    
    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        
        # Set shipping cost based on method
        shipping_method = cleaned_data.get('shipping_method')
        if shipping_method == 'standard':
            cleaned_data['shipping_cost'] = '0.00'
        elif shipping_method == 'express':
            cleaned_data['shipping_cost'] = '10.00'
        else:
            cleaned_data['shipping_cost'] = '25.00'
        
        return cleaned_data
