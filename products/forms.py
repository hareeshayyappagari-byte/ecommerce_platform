"""
Django Forms for products app.
Handles form validation and data collection for product-related operations.
"""

from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for adding and editing product reviews.
    Collects rating, title, and content from users.
    """
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} ⭐') for i in range(1, 6)]),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title',
                'maxlength': '100',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your detailed review here...',
                'rows': 5,
            }),
        }
    
    def clean_rating(self):
        """Validate rating is within valid range"""
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating
