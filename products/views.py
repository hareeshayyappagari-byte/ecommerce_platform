"""
View handlers for products app.
Handles product listing, searching, filtering, and product detail pages.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q, Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product, Category, Review
from .forms import ReviewForm


class ProductListView(ListView):
    """
    View to display list of all products on homepage.
    Supports filtering by category, searching, and sorting.
    """
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12  # Display 12 products per page
    
    def get_queryset(self):
        """
        Get queryset with filtering and search functionality.
        Filters products by category, search query, and availability.
        """
        queryset = Product.objects.filter(is_active=True)
        
        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(sku__icontains=search_query)
            )
        
        # Sort by selection
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['price', '-price', 'name', '-created_at']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add categories and featured products to context"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_products'] = Product.objects.filter(
            is_featured=True,
            is_active=True
        )[:4]
        context['current_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    """
    View to display detailed information about a single product.
    Shows product images, reviews, specifications, and recommendations.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'sku'  # Use SKU as URL parameter
    slug_url_kwarg = 'sku'
    
    def get_context_data(self, **kwargs):
        """Add reviews and related products to context"""
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Get reviews for product
        context['reviews'] = product.reviews.select_related('user').order_by('-created_at')
        
        # Calculate average rating
        avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = avg_rating or 0
        
        # Review count
        context['review_count'] = product.reviews.count()
        
        # Related products from same category
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        
        # Check if user already reviewed this product
        if self.request.user.is_authenticated:
            context['user_already_reviewed'] = product.reviews.filter(
                user=self.request.user
            ).exists()
        
        return context


@login_required
def add_review(request, sku):
    """
    View to handle adding a review for a product.
    Only authenticated users can add reviews.
    """
    product = get_object_or_404(Product, sku=sku)
    
    # Check if user already reviewed this product
    existing_review = product.reviews.filter(user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review.first())
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been posted successfully!')
            return redirect('products:product-detail', sku=sku)
    else:
        form = ReviewForm(instance=existing_review.first())
    
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/add_review.html', context)


def category_products(request, slug):
    """
    View to display products filtered by category.
    Shows all active products in a specific category.
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category=category,
        is_active=True
    )
    
    # Search within category
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'category': category,
        'products': products,
        'categories': Category.objects.all(),
    }
    return render(request, 'products/category_products.html', context)


def search_products(request):
    """
    View to handle product search functionality.
    Returns products matching search query across name, description, and SKU.
    """
    query = request.GET.get('q', '')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query),
            is_active=True
        )
    
    context = {
        'query': query,
        'products': products,
        'categories': Category.objects.all(),
    }
    return render(request, 'products/search_results.html', context)
