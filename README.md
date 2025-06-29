# E-commerce Site

A Django-based e-commerce website with product management, user authentication, and shopping cart functionality.

## Screenshots

![Home Page](https://i.imgur.com/your-image-id.png)
*Main landing page with featured products and categories*

![Product Listing](https://i.imgur.com/your-image-id.png)
*Product grid with filtering and sorting options*

![Shopping Cart](https://i.imgur.com/your-image-id.png)
*Shopping cart with product summary*

## Features

### User Features
- User authentication (login, register, logout)
- User profile management
- Password reset functionality
- Order history tracking

### Product Features
- Product listing with categories
- Product search functionality
- Product details with images
- Product reviews and ratings
- Product filtering and sorting

### Shopping Features
- Shopping cart functionality
- Wishlist
- Checkout process
- Order tracking
- Multiple payment options:
  - UPI Payment
  - Cash on Delivery (COD)
  - PayPal
  - Razorpay
  - Bank Transfer

### Admin Features
- Admin panel for product management
- Order management
- User management
- Category management
- Sales reports

## Screenshots

### Home Page
![Home Page](screenshots/home.png)
*Main landing page with featured products and categories*

### Product Listing
![Product Listing](screenshots/products.png)
*Product grid with filtering and sorting options*

### Product Details
![Product Details](screenshots/product-detail.png)
*Detailed product view with images and description*

### Shopping Cart
![Shopping Cart](screenshots/cart.png)
*Shopping cart with product summary*

### User Dashboard
![User Dashboard](screenshots/dashboard.png)
*User profile and order history*

### Admin Panel
![Admin Panel](screenshots/admin.png)
*Admin interface for managing products and orders*

## API Endpoints

### Authentication
- `/accounts/login/` - User login
- `/accounts/register/` - User registration
- `/accounts/logout/` - User logout
- `/accounts/password-reset/` - Password reset

### Products
- `/products/` - List all products
- `/products/<id>/` - Product details
- `/products/category/<category>/` - Products by category
- `/products/search/` - Search products

### Cart
- `/cart/` - View cart
- `/cart/add/<product_id>/` - Add to cart
- `/cart/remove/<product_id>/` - Remove from cart
- `/cart/update/<product_id>/` - Update cart quantity

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repository-url>
cd ecommerce_site
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `ecommerce_site/sample_settings.py` to `ecommerce_site/local_settings.py`
   - Update the settings in `local_settings.py` with your configuration

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Collect static files:
```bash
python manage.py collectstatic
```

8. Run the development server:
```bash
python manage.py runserver
```

9. Visit http://localhost:8000 in your browser

## Project Structure

- `ecommerce_site/` - Main project directory
  - `settings.py` - Project settings
  - `urls.py` - Main URL configuration
  - `wsgi.py` - WSGI configuration
  - `asgi.py` - ASGI configuration
- `shop/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions
  - `urls.py` - URL patterns
  - `forms.py` - Form definitions
  - `admin.py` - Admin configurations
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files
- `templates/` - HTML templates
- `requirements.txt` - Project dependencies
- `manage.py` - Django management script

## Troubleshooting

### Common Issues

1. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATIC_URL` in settings
   - Ensure `django.contrib.staticfiles` is in `INSTALLED_APPS`

2. **Media Files Not Uploading**
   - Check `MEDIA_ROOT` and `MEDIA_URL` in settings
   - Ensure media directory exists and has proper permissions

3. **Database Issues**
   - Delete `db.sqlite3` and run migrations again
   - Check database settings in `local_settings.py`

4. **Template Not Found**
   - Check template directory structure
   - Verify template name in view
   - Ensure app is in `INSTALLED_APPS`

### Development Tips

1. **Debug Mode**
   - Set `DEBUG = True` in `local_settings.py` for development
   - Never enable debug mode in production

2. **Secret Key**
   - Keep your secret key secure
   - Use environment variables in production

3. **Database**
   - Use SQLite for development
   - Use PostgreSQL for production

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or issues, please open an issue in the GitHub repository. 