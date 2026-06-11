# TechForge eCommerce Platform

Premium PC components, gaming peripherals, and custom-built PCs. Shop the best tech hardware with Linus Tech Tips-inspired design.

## Features

### 🛍️ **Product Catalog**
- **36 products** across 16 categories
- PC Components: CPUs, GPUs, Motherboards, RAM, Storage, Power Supplies, Cooling, Cases
- Gaming Accessories: Keyboards, Mice, Headsets, Monitors, Mousepads
- Custom PC Builds: Pre-built gaming rigs

### 🛠️ **Custom PC Builder**
- Select components and check compatibility in real-time
- Live price calculation
- Save builds for later
- Expert-tested configurations

### 👤 **User System**
- Registration & Authentication
- User Profiles with address management
- Order History
- Saved Custom Builds

### 🛒 **Shopping Cart & Checkout**
- Add/remove/update cart items
- Secure checkout flow
- Shipping calculation
- Order confirmation

### ⚡ **Tech Stack**
- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite (development)
- **No external frameworks** (React, Vue, Bootstrap, Tailwind)

## Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual environment

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Samrat-1267/ojt10.git
   cd ojt10/django/firstproject
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Seed sample data:
   ```bash
   python manage.py seed_data
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Products**: http://127.0.0.1:8000/products/
- **PC Builder**: http://127.0.0.1:8000/builder/
- **Cart**: http://127.0.0.1:8000/cart/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Login Credentials

- **Admin**: `admin` / `admin123`
- **Demo User**: `demo` / `demo123`

## Project Structure

```
project/
├── django/
│   └── firstproject/
│       ├── manage.py
│       ├── firstproject/
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       ├── apps/
│       │   ├── products/
│       │   ├── accounts/
│       │   ├── cart/
│       │   ├── orders/
│       │   └── custom_pc_builder/
│       ├── templates/
│       ├── static/
│       └── media/
├── README.md
└── requirements.txt
```

## Apps

### 1. Products
- Product catalog with categories
- Product details with specifications
- Reviews and ratings
- Search and filtering

### 2. Accounts
- User registration and authentication
- Profile management
- Address book
- Order history
- Saved builds

### 3. Cart
- Session-based or user-based cart
- Add/remove/update items
- Cart summary and shipping calculation

### 4. Orders
- Secure checkout flow
- Order review and confirmation
- Order history for users

### 5. Custom PC Builder
- Component selection with compatibility checking
- Real-time price calculation
- Save and load builds

## Design & UI

### Features
- **Modern dark theme** with premium aesthetics
- **Responsive design** for all devices
- **Smooth animations** and transitions
- **Linus Tech Tips** inspired tech aesthetic
- **Fast loading** with optimized assets

### Technologies Used
- **HTML5** for semantic markup
- **CSS3** with custom animations
- **Vanilla JavaScript** for interactivity
- **Django templates** for dynamic content

## Development Features

### Admin Panel
- Full CRUD for all models
- Product management with image uploads
- Order tracking and fulfillment
- User and address management

### Database Models
- **Category**: Product categories and subcategories
- **Product**: All products with specifications
- **Review**: Customer reviews and ratings
- **Cart/CartItem**: Shopping cart management
- **Order/OrderItem**: Order processing
- **SavedBuild**: Custom PC builds

### API Endpoints
- Product listing and details
- Authentication endpoints
- Cart management
- Checkout flow
- PC builder compatibility checking

## Sample Data

The database includes:

### Featured Products
- **AMD Ryzen 9 7950X** - $699.99 (Featured, Bestseller)
- **NVIDIA GeForce RTX 4090** - $1,799.99 (Featured, Bestseller)
- **ASUS ROG Crosshair X670E Hero** - $499.99 (Featured)
- **Wooting 60HE+** - $199.99 (Featured, Bestseller)

### Custom Builds
- **The Ultimate Gaming Rig** - $4,999.99 (Featured)
- **Streamer Pro Build** - $3,499.99 (Featured)
- **Value Gaming Build** - $1,499.99

### Reviews
- 10+ sample reviews across products
- Ratings from 4-5 stars
- Real customer feedback

## File Structure

### Templates
- `templates/base.html` - Main layout with navbar, footer
- `templates/home.html` - Homepage with featured products
- `templates/products/` - Product catalog and details
- `templates/accounts/` - User authentication and profiles
- `templates/cart/` - Shopping cart
- `templates/orders/` - Checkout flow
- `templates/custom_pc_builder/` - PC builder interface

### Static Files
- `static/css/style.css` - Main stylesheet
- `static/js/main.js` - General UI interactions
- `static/js/cart.js` - Cart functionality
- `static/js/pc_builder.js` - PC builder interactions

### Python Files
- All Django apps with models, views, urls, forms, admin
- Management command for data seeding

## How It Works

1. **User browses** the product catalog or uses the PC builder
2. **Adds items** to cart (session-based or user-authenticated)
3. **Checks out** with shipping information
4. **Reviews order** before final submission
5. **Receives confirmation** with order details
6. **Tracks order** in account history

## Future Enhancements

- Payment gateway integration (Stripe/PayPal)
- Advanced filtering and search
- Product comparison tool
- Wishlists
- Bulk ordering
- API for mobile apps

## License

This project is part of an educational exercise. All code is provided for learning purposes.

## Support

For issues or questions, please check the project documentation or contact the maintainer.