# Deployment Guide - Deploy to Render (Free Hosting)

This guide shows you how to deploy the ECommerce Platform to Render.com for FREE with complete functionality.

## 🌍 Why Render?

- ✅ **Free tier available** - No credit card required initially
- ✅ **PostgreSQL database** - Included free tier
- ✅ **GitHub integration** - Auto-deploy on push
- ✅ **Custom domains** - 6 free subdomains
- ✅ **SSL certificates** - Automatic HTTPS
- ✅ **24/7 monitoring** - Automatic health checks

## 📋 Prerequisites

1. GitHub account with your project repository
2. Render.com account (free signup)
3. Project files ready to push to GitHub

## 🚀 Step 1: Prepare Your Project

### 1.1 Create .env file

```bash
cp .env.example .env
```

### 1.2 Generate Secret Key

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the output and add to `.env`:
```
SECRET_KEY=your-generated-key-here
```

### 1.3 Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit - ECommerce Platform"
git branch -M main
git remote add origin https://github.com/yourusername/ecommerce-platform.git
git push -u origin main
```

## 🌐 Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Sign up" with GitHub
3. Authorize Render to access your GitHub
4. Complete account setup

## 🔧 Step 3: Create PostgreSQL Database

1. In Render dashboard, click "New +" button
2. Select **PostgreSQL**
3. Configure:
   - **Name**: ecommerce-db
   - **Database**: keep default
   - **User**: default user
   - **Region**: Choose closest to users
   - **PostgreSQL Version**: 14 or latest
4. Click **Create Database**
5. Wait 2-3 minutes for creation
6. Copy the **External Database URL** (save for next step)

## 🌟 Step 4: Create Web Service

1. In Render dashboard, click "New +" → **Web Service**
2. Connect your GitHub repository
3. Fill in configuration:

### Service Details
```
Name: ecommerce-platform
Runtime: Python 3
Region: Singapore (or closest to you)
Branch: main
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
Start Command: gunicorn core.wsgi
```

### Environment Variables

Click "Add Environment Variable" for each:

```
DEBUG=False
ALLOWED_HOSTS=*.onrender.com,your-custom-domain.com
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-postgres-url-here
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

# Email (Optional - for production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Instance Type
- Select **Free tier** for testing

4. Click **Create Web Service**

## ⏳ Step 5: Wait for Deployment

1. Render will automatically:
   - Install dependencies
   - Run migrations (from Procfile)
   - Start the application
2. Watch the deployment logs
3. Wait for "Service is live" message

## 🔐 Step 6: Initialize Database

1. Go to your Render dashboard
2. Click on your web service
3. Click "Shell" tab
4. Run initialization commands:

```bash
python manage.py migrate
python manage.py createsuperuser
# Follow prompts to create admin user
```

## 📊 Step 7: Add Sample Data

1. Go to `https://your-app-name.onrender.com/admin`
2. Login with your superuser credentials
3. Add categories and products:
   - Go to Products → Categories → Add Category
   - Go to Products → Products → Add Products

## 🌐 Step 8: Add Custom Domain (Optional)

1. In Render dashboard, go to your web service
2. Click the Settings tab
3. Under "Custom Domains", click "Add Custom Domain"
4. Enter your domain name
5. Follow DNS instructions from your domain provider
6. Render generates free SSL certificate automatically

## 🔄 Step 9: Auto-Deploy Setup

Every time you push to GitHub:

```bash
git add .
git commit -m "Update features"
git push origin main
```

Render automatically:
1. Pulls latest code
2. Installs dependencies
3. Runs migrations
4. Restarts the application

## 📱 Testing Your Deployment

### Check Application Status
```
https://your-app-name.onrender.com/
```

### Access Admin
```
https://your-app-name.onrender.com/admin/
```

### View Logs
1. Render dashboard → Your service
2. Click "Logs" tab
3. See real-time output

## 🐛 Troubleshooting

### "502 Bad Gateway" Error
```
Check logs for Python errors
Run: python manage.py check
Verify DATABASE_URL is set correctly
```

### "Static Files Not Found"
```
Ensure collect static ran in build command
Check static files were generated
Verify STATIC_URL configuration
```

### "Database Connection Error"
```
Copy DATABASE_URL directly from Render PostgreSQL
Remove extra parameters if needed
Test connection: psql $DATABASE_URL
```

### "Migration Errors"
```
SSH into Render shell
Run: python manage.py migrate --verbose
Check for conflicting migrations
```

## 📈 Monitoring & Performance

### View Metrics
1. Dashboard → Web Service
2. Click "Metrics" tab
3. Monitor:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

### Log Management
1. Go to "Logs" tab
2. Filter by:
   - Error level
   - Service component
   - Time range

## 💰 Pricing

### Free Tier Includes
- ✅ One free web service
- ✅ One free PostgreSQL database (0.5GB)
- ✅ 0.1 CPU cores
- ✅ 512 MB memory
- ✅ 100GB bandwidth per month
- ✅ Automatic HTTPS

### Paid Plans
- If needed, upgrade to paid plan
- Paid plans are very affordable
- Auto-upgrade when limit approaching

## 🔐 Security Best Practices

1. **Change Secret Key**: Generate new one for production
2. **Use HTTPS**: Enable SSL redirect
3. **Secure Cookies**: Set cookie secure flags
4. **Strong Passwords**: Use complex admin password
5. **Database Backup**: Enable Render backups
6. **Monitor Logs**: Check for suspicious activity

## 🚀 Next Steps

After deployment:

1. ✅ Verify application works
2. ✅ Test user registration
3. ✅ Test product catalog
4. ✅ Test shopping cart
5. ✅ Test checkout process
6. ✅ Add sample products
7. ✅ Configure email (optional)
8. ✅ Set up payment gateway (optional)

## 📞 Support

For Render support:
- [Render Documentation](https://render.com/docs)
- [Render Support](https://support.render.com)
- [Django Documentation](https://docs.djangoproject.com)

## ✅ Completion Checklist

- [ ] GitHub repository created
- [ ] PostgreSQL database created on Render
- [ ] Web service created on Render
- [ ] All environment variables set
- [ ] Application deployed successfully
- [ ] Database migrations completed
- [ ] Superuser created
- [ ] Admin panel accessible
- [ ] Sample data added
- [ ] Testing completed

---

**Congratulations! Your e-commerce platform is now live on Render! 🎉**

Visit: `https://your-app-name.onrender.com`
Admin: `https://your-app-name.onrender.com/admin`
