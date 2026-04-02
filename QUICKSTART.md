"""
Quick Start Guide - Running the ECommerce Platform Locally
============================================================

This guide helps you get the application running on your local machine in minutes.
"""

# =============================================================================
# STEP 1: CREATE VIRTUAL ENVIRONMENT
# =============================================================================
# This isolates project dependencies from your system Python

# macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv venv
venv\Scripts\activate


# =============================================================================
# STEP 2: INSTALL DEPENDENCIES
# =============================================================================
# Install all required Python packages listed in requirements.txt

pip install -r requirements.txt


# =============================================================================
# STEP 3: SETUP ENVIRONMENT VARIABLES
# =============================================================================
# Copy example environment file and configure settings

cp .env.example .env

# Edit .env file with your settings:
# - SECRET_KEY: Leave as default for development
# - DEBUG: Set to True for local development
# - ALLOWED_HOSTS: Keep as localhost,127.0.0.1


# =============================================================================
# STEP 4: CREATE DATABASE
# =============================================================================
# Run migrations to create database tables

python manage.py migrate


# =============================================================================
# STEP 5: CREATE ADMIN USER
# =============================================================================
# Create superuser account for accessing admin panel

python manage.py createsuperuser

# When prompted, enter:
# Username: admin (or your preferred username)
# Email: admin@example.com
# Password: Your secure password


# =============================================================================
# STEP 6: START DEVELOPMENT SERVER
# =============================================================================
# Run the Django development server

python manage.py runserver

# Server will start at: http://localhost:8000


# =============================================================================
# STEP 7: SETUP INITIAL DATA (OPTIONAL)
# =============================================================================
# Create sample products and categories

# Access admin panel:
# 1. Go to http://localhost:8000/admin
# 2. Login with your superuser credentials
# 3. Add categories under "Products" → "Categories"
# 4. Add products under "Products" → "Products"


# =============================================================================
# APPLICATION URLS
# =============================================================================

Homepage:           http://localhost:8000/
Admin Panel:        http://localhost:8000/admin/
Login:             http://localhost:8000/accounts/login/
Register:          http://localhost:8000/accounts/register/
Shopping Cart:     http://localhost:8000/cart/
Order History:     http://localhost:8000/orders/history/


# =============================================================================
# COMMON COMMANDS
# =============================================================================

# Run development server
python manage.py runserver

# Run migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Create a new Django app
python manage.py startapp app_name

# Access Django shell for testing
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Dump database data to file
python manage.py dumpdata > backup.json

# Load data from dump file
python manage.py loaddata backup.json

# Run tests
python manage.py test

# Check for common issues
python manage.py check


# =============================================================================
# TROUBLESHOOTING
# =============================================================================

# Issue: "ModuleNotFoundError: No module named 'django'"
# Solution: Make sure virtual environment is activated and dependencies installed

# Issue: "ConnectionRefusedError" for database
# Solution: Run 'python manage.py migrate' to create database

# Issue: Admin panel shows "Page not found"
# Solution: Check that DEBUG=True in .env

# Issue: Static files not loading
# Solution: Run 'python manage.py collectstatic' (for production)

# Issue: Port 8000 already in use
# Solution: python manage.py runserver 8001 (use different port)


# =============================================================================
# NEXT STEPS
# =============================================================================

# 1. Read the full README.md for detailed documentation
# 2. Explore the admin panel and create sample data
# 3. Test different features (cart, checkout, orders)
# 4. Review the codebase structure
# 5. Make modifications to customize for your needs
# 6. Deploy to Render when ready (see README.md for instructions)


# =============================================================================
# SUPPORT
# =============================================================================

# For issues, refer to:
# - README.md file in project root
# - Django documentation: https://docs.djangoproject.com/
# - Django REST Framework: https://www.django-rest-framework.org/
