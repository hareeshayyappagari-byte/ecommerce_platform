"""
View handlers for accounts app.
Handles user authentication, registration, profile management, and address management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import UserProfile, Address
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, AddressForm


@csrf_protect
@require_http_methods(['GET', 'POST'])
def register_user(request):
    """
    User registration view.
    Allows new users to create an account with email and password.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create new user
            user = form.save()
            # Log user in after registration
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to our store.')
            return redirect('products:home')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@csrf_protect
@require_http_methods(['GET', 'POST'])
def login_user(request):
    """
    User login view.
    Allows existing users to log into their accounts.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Get credentials from form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Redirect to next page or home
                next_page = request.GET.get('next', 'products:home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
@require_http_methods(['GET'])
def logout_user(request):
    """
    User logout view.
    Logs out the current user and clears session.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('products:home')


@login_required
def user_profile(request):
    """
    User profile view.
    Displays user information and allows editing profile details.
    """
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    # Get user addresses
    addresses = request.user.addresses.all()
    
    context = {
        'profile': profile,
        'form': form,
        'addresses': addresses,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def user_addresses(request):
    """
    User addresses view.
    Displays all saved addresses and allows management.
    """
    addresses = request.user.addresses.all()
    
    context = {
        'addresses': addresses,
    }
    return render(request, 'accounts/addresses.html', context)


@login_required
def add_address(request):
    """
    Add new address view.
    Allows users to add new shipping/billing addresses.
    """
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('accounts:addresses')
    else:
        form = AddressForm()
    
    context = {'form': form}
    return render(request, 'accounts/add_address.html', context)


@login_required
def edit_address(request, address_id):
    """
    Edit address view.
    Allows users to modify existing addresses.
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('accounts:addresses')
    else:
        form = AddressForm(instance=address)
    
    context = {
        'form': form,
        'address': address,
    }
    return render(request, 'accounts/edit_address.html', context)


@login_required
def delete_address(request, address_id):
    """
    Delete address view.
    Allows users to remove saved addresses.
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully!')
        return redirect('accounts:addresses')
    
    context = {'address': address}
    return render(request, 'accounts/confirm_delete_address.html', context)


@login_required
def set_default_address(request, address_id):
    """
    Set default address view.
    Marks an address as the default for future orders.
    """
    # Remove default flag from all user addresses
    request.user.addresses.all().update(is_default=False)
    
    # Set selected address as default
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.is_default = True
    address.save()
    
    messages.success(request, 'Default address updated!')
    return redirect('accounts:addresses')
