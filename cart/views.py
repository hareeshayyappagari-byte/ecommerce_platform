"""
View handlers for cart app.
Manages shopping cart operations - add, remove, update, and checkout.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from .models import Cart, CartItem
from products.models import Product


def get_or_create_cart(request):
    """
    Helper function to get or create cart.
    Uses user ID for authenticated users or session for anonymous users.
    """
    if request.user.is_authenticated:
        # Get cart for authenticated user
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Get cart for anonymous user using session
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    return cart


def view_cart(request):
    """
    View shopping cart page.
    Displays all items in the cart with totals and checkout button.
    """
    cart = get_or_create_cart(request)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product'),
        'cart_total': cart.get_total_price(),
        'cart_items_count': cart.get_total_items_count(),
    }
    return render(request, 'cart/view_cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    """
    Add product to cart (POST request only).
    Accepts quantity as POST parameter, defaults to 1.
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    
    # Get quantity from request, default to 1
    quantity = int(request.POST.get('quantity', 1))
    
    # Validate quantity
    if quantity < 1:
        quantity = 1
    if quantity > product.stock_quantity:
        messages.warning(request, f'Only {product.stock_quantity} items available in stock.')
        quantity = product.stock_quantity
    
    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Update quantity if item already exists
        old_quantity = cart_item.quantity
        cart_item.quantity = min(quantity + old_quantity, product.stock_quantity)
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    
    # Return to previous page or product page
    return redirect(request.GET.get('next', 'products:home'))


@require_POST
def remove_from_cart(request, item_id):
    """
    Remove item from cart (POST request only).
    """
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('cart:view')


@require_POST
def update_cart_quantity(request, item_id):
    """
    Update quantity of cart item (POST request only).
    Accepts new quantity as POST parameter.
    """
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    # Get new quantity
    new_quantity = int(request.POST.get('quantity', 1))
    
    # Validate quantity
    if new_quantity < 1:
        new_quantity = 1
    if new_quantity > cart_item.product.stock_quantity:
        messages.warning(request, f'Only {cart_item.product.stock_quantity} items available.')
        new_quantity = cart_item.product.stock_quantity
    
    cart_item.quantity = new_quantity
    cart_item.save()
    
    messages.success(request, 'Cart updated!')
    return redirect('cart:view')


@require_POST
def clear_cart(request):
    """
    Clear all items from cart (POST request only).
    """
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    
    messages.success(request, 'Cart cleared!')
    return redirect('cart:view')


def cart_context(request):
    """
    Context processor to add cart information to all templates.
    Makes cart accessible in every template context.
    """
    cart = get_or_create_cart(request)
    return {
        'cart': cart,
        'cart_items_count': cart.get_total_items_count(),
    }


@require_http_methods(['GET'])
def get_cart_count(request):
    """
    API endpoint to get current cart item count.
    Returns JSON response for AJAX requests.
    """
    cart = get_or_create_cart(request)
    return JsonResponse({
        'count': cart.get_total_items_count(),
        'total': str(cart.get_total_price()),
    })
