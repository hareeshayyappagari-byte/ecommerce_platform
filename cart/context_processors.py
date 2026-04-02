"""
Context processors for cart app.
Provides cart information to all templates.
"""

from .models import Cart


def cart_context(request):
    """
    Context processor that adds cart to every template.
    Makes cart data available in all template contexts.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # For anonymous users, create using session
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    return {
        'cart': cart,
        'cart_items_count': cart.get_total_items_count(),
        'cart_total': cart.get_total_price(),
    }
