# Development Reference Guide

## 📚 Code Documentation Standards

All code in this project follows professional Python and Django conventions.

### Comment Format

```python
"""
Function/Module docstring explaining purpose.
Describes what the code does, not how.
"""

# Single line comment for implementation details
code_here()

# Multi-line comment for complex logic
# explaining step-by-step what happens
value = calculate()
```

### Example: Function with Comments

```python
def process_order(user, cart, payment_method):
    """
    Process customer order from shopping cart.
    
    Creates order record, reduces inventory, and triggers
    notification emails.
    
    Args:
        user: User object placing the order
        cart: Shopping cart instance
        payment_method: Selected payment method
    
    Returns:
        Order: Created order instance
    
    Raises:
        ValueError: If cart is empty or inventory insufficient
    """
    # Validate cart has items
    if cart.is_empty():
        raise ValueError("Cart cannot be empty")
    
    # Calculate order total
    subtotal = cart.get_total_price()  # Sum of all items
    tax = subtotal * SETTINGS.TAX_RATE  # Apply tax rate
    total = subtotal + tax  # Final amount due
    
    # Create order record in database
    order = Order.objects.create(
        customer=user,
        total_amount=total,
        payment_method=payment_method,
    )
    
    return order
```

## 🏗️ File Organization

### Models (models.py)
- One model = one class
- Related models grouped together
- Meta class with ordering and indexes
- Custom methods follow model behavior

### Views (views.py)
- One view = one functionality
- Function-based or class-based
- Comments explaining business logic
- Error handling with try/except

### Forms (forms.py)
- One form = one model or operation
- Field validation in clean methods
- Widget configuration with Bootstrap classes

### URLs (urls.py)
- Routes organized by feature
- Descriptive URL patterns
- Namespace for app separation

### Templates (templates/)
- Structure: templates/app_name/template.html
- Extends base template
- Comments in complex sections

## 🔧 Common Development Tasks

### Add New Model

```python
# 1. Create model in models.py
class NewModel(models.Model):
    """Your model description"""
    field1 = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

# 2. Create migration
python manage.py makemigrations

# 3. Apply migration
python manage.py migrate

# 4. Register in admin.py
@admin.register(NewModel)
class NewModelAdmin(admin.ModelAdmin):
    list_display = ['field1', 'created_at']
```

### Add New View

```python
# 1. Create view in views.py
def my_view(request):
    """View description"""
    context = {'data': 'value'}
    return render(request, 'template.html', context)

# 2. Add URL in urls.py
path('my-url/', views.my_view, name='my-view')

# 3. Create template
# templates/app/template.html
```

### Add New Form

```python
# 1. Create form in forms.py
class MyForm(forms.Form):
    """Form description"""
    field = forms.CharField(max_length=100)

# 2. Use in view
form = MyForm(request.POST)
if form.is_valid():
    # Process form
    pass

# 3. Display in template
{{ form.as_p }}
```

## 🧪 Testing Guide

### Run All Tests
```bash
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test products
python manage.py test accounts
```

### Run Specific Test Class
```bash
python manage.py test products.tests.ProductModelTest
```

### Run Specific Test Method
```bash
python manage.py test products.tests.ProductModelTest.test_product_creation
```

### Test with Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🐛 Debugging

### Django Shell
```bash
python manage.py shell

# Now you can run Python code
from products.models import Product
Product.objects.all()
p = Product.objects.first()
p.name
```

### Print Debugging
```python
# Add debug print statements
print(f"DEBUG: {variable_name}")

# View in console when running dev server
python manage.py runserver
```

### Django Debug Toolbar
```bash
# Install
pip install django-debug-toolbar

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Set INTERNAL_IPS
INTERNAL_IPS = ['127.0.0.1']
```

## 📊 Database Queries

### Common Query Patterns

```python
# Get all products
products = Product.objects.all()

# Filter products
electronics = Product.objects.filter(category__name='Electronics')

# Get single product
product = Product.objects.get(sku='SKU-001')

# Check if exists
exists = Product.objects.filter(sku='SKU-001').exists()

# Count objects
count = Product.objects.count()

# Order results
sorted_products = Product.objects.order_by('-created_at')

# Limit results
first_10 = Product.objects.all()[:10]

# Exclude results
not_featured = Product.objects.exclude(is_featured=True)

# Multiple filters (AND)
result = Product.objects.filter(category__name='Electronics', price__lt=100)

# Multiple filters (OR)
from django.db.models import Q
result = Product.objects.filter(Q(price__lt=100) | Q(is_featured=True))

# Count related objects
products_with_reviews = Product.objects.annotate(review_count=Count('reviews'))

# Get related objects
category_products = category.products.all()

# Prefetch related (performance optimization)
products = Product.objects.prefetch_related('reviews', 'images')
```

## 🎨 Template Tags & Filters

### Common Tags
```django
<!-- If statement -->
{% if user.is_authenticated %}
    Logged in
{% else %}
    Not logged in
{% endif %}

<!-- For loop -->
{% for product in products %}
    {{ product.name }}
{% endfor %}

<!-- Include template -->
{% include 'partial_template.html' %}

<!-- CSRF protection -->
{% csrf_token %}

<!-- URL reverse -->
<a href="{% url 'app:view-name' %}">Link</a>
```

### Common Filters
```django
<!-- String filters -->
{{ product.name|upper }}
{{ product.name|lower }}
{{ product.name|title }}
{{ product.name|truncatewords:5 }}

<!-- Numeric filters -->
{{ product.price|floatformat:2 }}
{{ products|length }}

<!-- Date filters -->
{{ order.created_at|date:"M d, Y" }}
{{ order.created_at|date:"h:i A" }}

<!-- URL filters -->
{{ 'hello world'|slugify }}
```

## 🚀 Performance Optimization

### Database Query Optimization
```python
# BAD - N+1 query problem
for order in Order.objects.all():
    print(order.customer.username)  # Extra query per loop

# GOOD - Prefetch related
orders = Order.objects.prefetch_related('customer')
for order in orders:
    print(order.customer.username)  # No extra queries

# GOOD - Select related
orders = Order.objects.select_related('customer')
for order in orders:
    print(order.customer.username)
```

### Template Caching
```django
{% load cache %}

{% cache 500 product_detail product.id %}
    <!-- Expensive to render content -->
    {{ product.description|safe }}
{% endcache %}
```

### Static Files Optimization
- Use `whitenoise` for serving static files
- Minimize CSS/JS files
- Use CDN for large files (optional)
- Compress images

## 📝 Version Control Tips

### Commit Messages
```
Good:
- "Add product search functionality"
- "Fix cart total calculation bug"
- "Update user registration form"

Bad:
- "update"
- "fixes"
- "changes stuff"
```

### Branch Naming
```
Feature: feature/product-search
Bug Fix: bugfix/cart-calculation
Release: release/v1.0.0
```

### Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "Add new feature"

# Push to GitHub
git push origin feature/new-feature

# Create Pull Request on GitHub
# After review, merge to main
```

## 🔒 Security Checklist

- [ ] SECRET_KEY is unique and secure
- [ ] DEBUG is False in production
- [ ] ALLOWED_HOSTS is configured
- [ ] HTTPS is enabled
- [ ] CSRF protection is enabled
- [ ] SQL injection is prevented
- [ ] XSS attacks are prevented
- [ ] Passwords are hashed
- [ ] Sensitive data in .env
- [ ] Dependencies are updated

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com)
- [Django REST Framework](https://www.django-rest-framework.org)
- [Django Security](https://docs.djangoproject.com/en/dev/topics/security/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Naming Conventions](https://google.github.io/styleguide/pyguide.html)

---

For more specific help, refer to code comments in the respective modules.
