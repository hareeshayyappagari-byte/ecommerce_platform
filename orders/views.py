"""
View handlers for orders app.
Handles order creation, checkout, payment, order tracking, and history.
"""

import logging
from decimal import Decimal
import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from .models import Order, OrderItem, OrderTracking
from cart.models import Cart
from accounts.models import Address
from .forms import CheckoutForm

logger = logging.getLogger('ecommerce')


def generate_order_number():
    """Generate unique order number"""
    return f"ORD-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    """
    Checkout view.
    Handles order creation, address selection, and payment method selection.
    """
    try:
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or cart.is_empty():
            messages.warning(request, 'Your cart is empty!')
            return redirect('cart:view')

        addresses = request.user.addresses.all()
        default_address = addresses.filter(is_default=True).first()

        if request.method == 'POST':
            form = CheckoutForm(request.POST, user=request.user)
            if form.is_valid():
                with transaction.atomic():
                    order = create_order(
                        request.user,
                        cart,
                        form.cleaned_data
                    )

                cart.items.all().delete()
                messages.success(request, f'Order {order.order_number} created successfully!')
                return redirect('orders:order-detail', order_id=order.id)
        else:
            initial_data = {}
            if default_address:
                initial_data['shipping_address'] = default_address.id
                initial_data['billing_address'] = default_address.id

            form = CheckoutForm(user=request.user, initial=initial_data)

        context = {
            'form': form,
            'cart': cart,
            'cart_total': cart.get_total_price(),
            'addresses': addresses,
        }
        return render(request, 'orders/checkout.html', context)

    except Exception:
        logger.exception('Checkout exception for user %s', request.user)
        messages.error(request, 'Unable to process checkout right now. Please try again.')
        return redirect('cart:view')


def create_order(customer, cart, form_data):
    """
    Create order from cart data and form input.
    Handles all order creation logic and initializations.
    """
    try:
        shipping_address = Address.objects.get(
            id=form_data['shipping_address'],
            user=customer
        )

        billing_address = None
        if form_data.get('billing_address'):
            billing_address = Address.objects.get(
                id=form_data['billing_address'],
                user=customer
            )

        subtotal = cart.get_total_price()
        shipping_cost = Decimal(form_data.get('shipping_cost', '0.00'))
        tax = (subtotal * Decimal('0.18'))
        discount = Decimal(form_data.get('discount', '0.00'))
        total = subtotal + shipping_cost + tax - discount

        order = Order.objects.create(
            order_number=generate_order_number(),
            customer=customer,
            shipping_address=shipping_address,
            billing_address=billing_address,
            status='confirmed',
            payment_method=form_data.get('payment_method', 'cod'),
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            discount=discount,
            total_amount=total,
            coupon_code=form_data.get('coupon_code'),
            notes=form_data.get('notes'),
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_price=cart_item.get_item_price(),
                product_sku=cart_item.product.sku,
                quantity=cart_item.quantity,
            )
            cart_item.product.stock_quantity -= cart_item.quantity
            cart_item.product.save()

        OrderTracking.objects.create(
            order=order,
            status='confirmed',
            description='Your order has been confirmed and is being processed.',
        )

        if form_data.get('payment_method') == 'cod':
            order.payment_status = 'pending'
        else:
            order.payment_status = 'pending'

        order.save()
        return order

    except Exception:
        logger.exception('Failed to create order for user %s', customer)
        raise


@login_required
def order_detail(request, order_id):
    """
    Order detail view.
    Displays complete order information, items, and tracking history.
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    # Get tracking updates
    tracking_updates = order.tracking_updates.all()
    
    context = {
        'order': order,
        'order_items': order.items.all(),
        'tracking_updates': tracking_updates,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_history(request):
    """
    Order history view.
    Displays list of all orders placed by the user.
    """
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    # Pagination support
    from django.core.paginator import Paginator
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'orders': page_obj.object_list,
    }
    return render(request, 'orders/order_history.html', context)


@login_required
def cancel_order(request, order_id):
    """
    Cancel order view.
    Allows user to cancel pending orders.
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    # Check if order can be cancelled
    if order.status not in ['pending', 'confirmed']:
        messages.error(request, 'This order cannot be cancelled.')
        return redirect('orders:order-detail', order_id=order.id)
    
    if request.method == 'POST':
        # Cancel order
        order.status = 'cancelled'
        order.save()
        
        # Restore stock
        for item in order.items.all():
            if item.product:
                item.product.stock_quantity += item.quantity
                item.product.save()
        
        # Add tracking update
        OrderTracking.objects.create(
            order=order,
            status='cancelled',
            description='Order has been cancelled.',
        )
        
        messages.success(request, 'Order cancelled successfully!')
        return redirect('orders:history')
    
    context = {'order': order}
    return render(request, 'orders/confirm_cancel.html', context)


@login_required
def track_order(request, order_id):
    """
    Track order view.
    Shows real-time tracking information and status updates.
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    tracking_updates = order.tracking_updates.all().order_by('-timestamp')
    
    context = {
        'order': order,
        'tracking_updates': tracking_updates,
    }
    return render(request, 'orders/track_order.html', context)
