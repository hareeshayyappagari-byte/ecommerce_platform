# 🛒 ECommerce Platform - Professional Django E-Commerce Application

A fully-featured, production-ready e-commerce platform built with Django, featuring user authentication, product catalog, shopping cart, order management, and admin dashboard.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running Locally](#running-locally)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Deployment on Render](#deployment-on-render)
- [Admin Panel](#admin-panel)
- [Contributing](#contributing)

## ✨ Features

### User Management
- ✅ User registration and authentication
- ✅ User profile management
- ✅ Address management (shipping, billing)
- ✅ User dashboard

### Product Management
- ✅ Product catalog with images
- ✅ Product categories
- ✅ Product search and filtering
- ✅ Product reviews and ratings
- ✅ Discount pricing
- ✅ Stock management

### Shopping Cart
- ✅ Add/remove items from cart
- ✅ Update item quantities
- ✅ Cart persistence
- ✅ Real-time cart updates

### Order Management
- ✅ Checkout process
- ✅ Order creation with validation
- ✅ Order history
- ✅ Order tracking
- ✅ Order cancellation
- ✅ Multiple payment methods support

### Admin Dashboard
- ✅ Product management
- ✅ Category management
- ✅ Order management
- ✅ Customer management
- ✅ Review moderation

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (production) |
| Frontend | HTML5, Bootstrap 5, CSS3, JavaScript |
| Web Server | Gunicorn |
| Deployment | Render |
| Authentication | Django built-in |
| Forms | Django Forms |

## 📁 Project Structure

```
ecommerce_platform/
├── core/                          # Main Django configuration
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   ├── wsgi.py                   # WSGI application
│   └── asgi.py                   # ASGI application
│
├── products/                      # Product management app
│   ├── models.py                 # Product, Category, Review models
│   ├── views.py                  # Product list, detail views
│   ├── admin.py                  # Admin configuration
│   ├── forms.py                  # Product forms
│   ├── urls.py                   # Product URLs
│   └── templates/
│       ├── product_list.html     # Product catalog page
│       └── product_detail.html   # Product detail page
│
├── accounts/                      # User account management
│   ├── models.py                 # User profile, Address models
│   ├── views.py                  # Login, registration, profile views
│   ├── admin.py                  # Admin configuration
│   ├── forms.py                  # User forms
│   ├── urls.py                   # Account URLs
│   └── templates/
│       ├── login.html            # Login page
│       ├── register.html         # Registration page
│       └── profile.html          # User profile page
│
├── cart/                          # Shopping cart management
│   ├── models.py                 # Cart, CartItem models
│   ├── views.py                  # Add to cart, remove, update views
│   ├── admin.py                  # Admin configuration
│   ├── urls.py                   # Cart URLs
│   ├── context_processors.py     # Cart context processor
│   └── templates/
│       └── view_cart.html        # Shopping cart page
│
├── orders/                        # Order management
│   ├── models.py                 # Order, OrderItem, OrderTracking models
│   ├── views.py                  # Checkout, order history views
│   ├── admin.py                  # Admin configuration
│   ├── forms.py                  # Checkout form
│   ├── urls.py                   # Order URLs
│   └── templates/
│       ├── checkout.html         # Checkout page
│       ├── order_history.html    # Order history page
│       └── order_detail.html     # Order detail page
│
├── templates/
│   └── base/
│       └── base.html             # Base template with navbar and footer
│
├── static/                        # Static files (CSS, JS, images)
│   ├── css/                      # Custom CSS files
│   ├── js/                       # JavaScript files
│   └── images/                   # Static images
│
├── media/                         # User uploaded files
│   ├── products/                 # Product images
│   └── profiles/                 # User profile pictures
│
├── db.sqlite3                    # SQLite database (development)
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── Procfile                      # Render deployment configuration
├── runtime.txt                   # Python version for deployment
└── README.md                     # This file
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv or venv
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ecommerce_platform
```

### Step 2: Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

### Step 5: Run Migrations

```bash
# Create database tables
python manage.py migrate
```

### Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Step 7: Collect Static Files (Optional for development)

```bash
python manage.py collectstatic --noinput
```

## ⚙️ Configuration

### Important Settings in `core/settings.py`:

#### Database Configuration
```python
# Development (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production (PostgreSQL via DATABASE_URL)
if config('DATABASE_URL', default=None):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
```

#### Email Configuration
```python
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
```

#### Security Settings
```python
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
```

## 🏃 Running Locally

### Start Development Server

```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`

### Admin Panel

Navigate to: `http://localhost:8000/admin`

Use your superuser credentials to login.

### Test User Data

Create sample products and categories through the admin panel:

1. Go to `/admin`
2. Login with superuser
3. Add categories under "Products" → "Categories"
4. Add products under "Products" → "Products"

## 🗄️ Database Models

### Products App

**Category Model**
```python
- name: CharField - Category name
- description: TextField - Category description
- slug: SlugField - URL-friendly identifier
```

**Product Model**
```python
- name: CharField - Product name
- description: TextField - Detailed description
- sku: CharField - Stock Keeping Unit
- category: ForeignKey - Category reference
- price: DecimalField - Regular price
- discount_price: DecimalField - Discounted price (optional)
- image: ImageField - Product image
- stock_quantity: IntegerField - Available inventory
- is_featured: BooleanField - Featured product flag
- is_active: BooleanField - Active/inactive status
```

**Review Model**
```python
- product: ForeignKey - Product being reviewed
- user: ForeignKey - User who wrote review
- rating: IntegerField - 1-5 star rating
- title: CharField - Review title
- content: TextField - Review text
```

### Accounts App

**UserProfile Model**
```python
- user: OneToOneField - User reference
- phone_number: CharField
- date_of_birth: DateField
- profile_picture: ImageField
- bio: TextField
- account_type: CharField - Individual or Business
- is_newsletter_subscribed: BooleanField
```

**Address Model**
```python
- user: ForeignKey - User who owns address
- address_type: CharField - Billing/Shipping/Default
- full_name: CharField
- street_address_line_1: CharField
- street_address_line_2: CharField (optional)
- city: CharField
- state: CharField
- postal_code: CharField
- country: CharField
- phone_number: CharField
- is_default: BooleanField
```

### Cart App

**Cart Model**
```python
- user: OneToOneField - User owner
- session_key: CharField - Anonymous user session
- created_at: DateTimeField
- updated_at: DateTimeField
```

**CartItem Model**
```python
- cart: ForeignKey - Parent cart
- product: ForeignKey - Product in cart
- quantity: PositiveIntegerField
```

### Orders App

**Order Model**
```python
- order_number: CharField - Unique order ID
- customer: ForeignKey - Customer user
- shipping_address: ForeignKey - Shipping address
- billing_address: ForeignKey - Billing address
- status: CharField - Order status
- payment_status: CharField - Payment status
- payment_method: CharField - Payment method
- subtotal: DecimalField
- shipping_cost: DecimalField
- tax: DecimalField
- discount: DecimalField
- total_amount: DecimalField - Final price
```

**OrderItem Model**
```python
- order: ForeignKey - Parent order
- product: ForeignKey - Product ordered
- product_name: CharField - Snapshot of product name
- product_price: DecimalField - Price at time of order
- quantity: PositiveIntegerField
```

## 📡 API Endpoints

### Products
- `GET /` - Product listing with filters
- `GET /product/<sku>/` - Product detail
- `POST /product/<sku>/review/` - Add product review
- `GET /category/<slug>/` - Products by category
- `GET /search/` - Product search

### Accounts
- `GET /accounts/register/` - Registration page
- `POST /accounts/register/` - Register user
- `GET /accounts/login/` - Login page
- `POST /accounts/login/` - Login user
- `GET /accounts/logout/` - Logout user
- `GET /accounts/profile/` - User profile
- `GET /accounts/addresses/` - User addresses
- `POST /accounts/address/add/` - Add address

### Cart
- `GET /cart/` - View cart
- `POST /cart/add/<product_id>/` - Add to cart
- `POST /cart/remove/<item_id>/` - Remove from cart
- `POST /cart/update/<item_id>/` - Update quantity
- `POST /cart/clear/` - Clear cart

### Orders
- `GET /orders/checkout/` - Checkout page
- `POST /orders/checkout/` - Create order
- `GET /orders/<order_id>/` - Order detail
- `GET /orders/history/` - Order history
- `GET /orders/<order_id>/track/` - Track order
- `POST /orders/<order_id>/cancel/` - Cancel order

## 🌐 Deployment on Render

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub or email
3. Connect your GitHub repository

### Step 2: Create New Web Service

1. Click "New +" → "Web Service"
2. Select your repository
3. Fill in service details:
   - **Name**: ecommerce-platform
   - **Region**: Choose closest to users
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn core.wsgi`

### Step 3: Set Environment Variables

1. In Render dashboard, go to "Environment"
2. Add environment variables:
   ```
   DEBUG=False
   ALLOWED_HOSTS=your-app.onrender.com
   SECRET_KEY=<generate-new-key>
   DATABASE_URL=<postgresql-url>
   ```

3. Generate new secret key:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

### Step 4: Database Setup

1. Create PostgreSQL database on Render
2. Copy DATABASE_URL
3. Add to environment variables
4. Render will auto-run migrations from Procfile

### Step 5: Deploy

1. Push code to GitHub
2. Render auto-deploys on push
3. Check deployment logs
4. Visit your app URL

### Step 6: Create Admin User

```bash
# After deployment, run in Render shell
python manage.py createsuperuser
```

## 👨‍💼 Admin Panel

Access admin at: `/admin`

### Admin Features:

**Products Management**
- Create/edit/delete products
- Manage categories
- Review moderation
- Inventory tracking

**Orders Management**
- View all orders
- Update order status
- Track shipments
- Print invoices

**Users Management**
- View user profiles
- Manage addresses
- Edit user information

**Site Administration**
- Customize site settings
- Manage permissions
- View system logs

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📝 Code Comments & Documentation

All code includes detailed comments explaining:
- Function purpose and parameters
- Model field descriptions
- Business logic explanations
- Important configuration details

## 🔒 Security Features

- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ Secure password hashing
- ✅ SQL parameterization
- ✅ Session security
- ✅ Admin authentication

## 📞 Support

For issues and questions:
1. Check existing GitHub issues
2. Create new issue with details
3. Follow issue template

## 📄 License

This project is licensed under MIT License - see LICENSE file.

## 🎉 Credits

Built with Django - The Web framework for perfectionists with deadlines.

---

**Made with ❤️ by Your Development Team**

Last Updated: 2024
Version: 1.0.0
