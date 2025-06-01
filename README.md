# E-commerce Site

A Django-based e-commerce website with product management, user authentication, and shopping cart functionality.

## Features

- User authentication (login, register, logout)
- Product listing and details
- Shopping cart functionality
- Admin panel for product management
- Responsive design

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
- `shop/` - Main application directory
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files
- `templates/` - HTML templates

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 