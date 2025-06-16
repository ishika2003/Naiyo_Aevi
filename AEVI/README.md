# 🌿 AEVI - Pure Nordic Skincare Platform

A complete Flask backend + frontend integration for AEVI's Nordic skincare e-commerce platform, replicating the functionalities of [liveaevi.com](https://liveaevi.com).

## ✨ Features

### 🏠 **Frontend**

- **Multi-page system** - About, Shop, Contact, Blog pages with SEO-friendly URLs
- **Responsive design** - Mobile-first approach with existing CSS/JS preserved
- **Dynamic content loading** - Products loaded via Flask API endpoints
- **Search functionality** - Real-time product search
- **Newsletter integration** - Modal subscription with 10% discount

### 🔧 **Backend (Flask)**
- **Routing system** - Clean URLs without .html extensions
- **PostgreSQL database** - Scalable data storage
- **User authentication** - Sign up/sign in with Flask-Login
- **Session management** - Secure user sessions
- **Email integration** - Contact forms and newsletters via Flask-Mail
- **API endpoints** - RESTful API for frontend integration
- **Admin dashboard** - User profile management

### 🛒 **E-commerce Features**
- **Product catalog** - Dynamic product display with categories
- **Bestsellers & New items** - Special product badges
- **Shopping filters** - Category-based product filtering
- **Product ratings** - Star ratings and review counts
- **Contact forms** - Lead generation and customer support
- **Newsletter system** - Email marketing integration

### 🔐 **Authentication & Security**
- **User registration** - Account creation with email verification
- **Secure login** - Password hashing with Werkzeug
- **Protected routes** - Login-required pages
- **Session management** - Automatic logout and security
- **CSRF protection** - Form security

### 📊 **Database Models**
- **Users** - Authentication and profile management
- **Products** - Skincare product catalog
- **Newsletter** - Email subscription management
- **Leads** - Contact form submissions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- Git

### 1. **Clone & Setup**
```bash
git clone <repository>
cd AEVI-main

# Run automated setup
python setup.py
```

### 2. **Manual Setup (Alternative)**
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py

# Run the application
python app.py
```

### 3. **Access the Application**
- **Homepage**: http://localhost:5000
- **Shop**: http://localhost:5000/shop
- **About**: http://localhost:5000/about
- **Contact**: http://localhost:5000/contact
- **Admin Dashboard**: http://localhost:5000/dashboard

## 🏗️ Project Structure

```
AEVI-main/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization script
├── setup.py              # Automated setup script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # This file
│
├── templates/           # Jinja2 templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Homepage (preserved original)
│   ├── about.html      # About page
│   ├── shop.html       # Product catalog
│   ├── contact.html    # Contact form
│   ├── signin.html     # User authentication
│   ├── signup.html     # User registration
│   ├── dashboard.html  # User dashboard
│   ├── navbar.html     # Navigation component
│   ├── footer.html     # Footer component
│   ├── 404.html        # Error pages
│   └── 500.html
│
├── static/             # Static assets
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   ├── images/        # Images and media
│   └── icomoon/       # Icon fonts
│
└── logs/              # Application logs
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database
DATABASE_URL=postgresql://user:pass@localhost/aevi_db

# Email (for contact forms & newsletters)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Setup Options

**PostgreSQL (Production)**
```bash
# Create database
createdb aevi_db

# Set DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost/aevi_db
```

**SQLite (Development)**
```bash
# Set DATABASE_URL in .env
DATABASE_URL=sqlite:///aevi.db
```

## 🔗 API Endpoints

### Products
- `GET /api/products` - All products
- `GET /api/products/bestsellers` - Bestseller products
- `GET /api/products/new` - New products
- `GET /api/products/category/<category>` - Products by category
- `GET /api/search?q=<query>` - Search products

### Authentication
- `POST /signin` - User sign in
- `POST /signup` - User registration
- `GET /logout` - User logout
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile

### Forms & Newsletter
- `POST /submit-contact` - Contact form submission
- `POST /subscribe-newsletter` - Newsletter subscription
- `POST /api/newsletter/unsubscribe` - Newsletter unsubscribe
### Flask URL Integration
```html
<!-- Navigation links -->
<a href="{{ url_for('shop') }}">SHOP</a>
<a href="{{ url_for('about') }}">ABOUT</a>
<a href="{{ url_for('contact') }}">CONTACT</a>

<!-- Static files -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
```

### Dynamic Content Loading
```javascript
// Load products dynamically
fetch('/api/products')
    .then(response => response.json())
    .then(products => renderProducts(products));

// Newsletter subscription
fetch('/subscribe-newsletter', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email })
});
```

## 🧪 Test Data

The application includes sample data replicating the live website:

### Test Users
- **Admin**: admin@aevi.com / admin123
- **User**: user@example.com / password123
- **User**: jane@example.com / password123

### Sample Products
- Nourishing Face Oil (€98) - Bestseller
- Hyaluronic Acid Face Serum (€94) - Bestseller  
- All-Over Balm (€24) - Bestseller
- Clarifying Clay Mask (€38) - New
- Cloud Bag (€22) - New
- Body care products and gift sets

## 🚀 Deployment

### Heroku Deployment
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-postgres-url

# Deploy
git add .
git commit -m "Deploy AEVI Flask app"
git push heroku main
```

### Environment Variables for Production
```bash
SECRET_KEY=secure-random-key
DATABASE_URL=postgresql://...
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
FLASK_ENV=production
```

## 🛠️ Development

### Adding New Features
1. **Models** - Add to `app.py` database models
2. **Routes** - Create new routes for pages/API endpoints
3. **Templates** - Add Jinja2 templates in `templates/`
4. **Static Files** - Add CSS/JS to `static/`

### Database Migrations
```bash
# Reset database (development)
python init_db.py

# Add new sample data
# Edit init_db.py and re-run
```

### Testing
```bash
# Run with debug mode
python app.py

# Test specific routes
curl http://localhost:5000/api/products
```

## 📱 Mobile Responsiveness

The platform is fully responsive with:
- Mobile-first CSS design
- Touch-friendly navigation
- Optimized product galleries
- Responsive forms and modals

## 🔒 Security Features

- **Password Hashing** - Werkzeug secure hashing
- **Session Management** - Flask-Login integration
- **CSRF Protection** - Form security tokens
- **Input Validation** - Server-side validation
- **SQL Injection Prevention** - SQLAlchemy ORM
- **XSS Protection** - Jinja2 auto-escaping

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For questions or issues:
- **Email**: Contact form at /contact
- **Issues**: GitHub Issues
- **Documentation**: This README



## 🌟 Key Achievements

✅ **Homepage Preserved** - Original design completely unchanged  
✅ **Flask Backend** - Complete Python backend with PostgreSQL  
✅ **User Authentication** - Sign up/sign in functionality  
✅ **Product Catalog** - Dynamic product loading from database  
✅ **Contact Forms** - Lead generation and email notifications  
✅ **Newsletter System** - Email marketing integration  
✅ **Mobile Responsive** - Works on all devices  
✅ **SEO Friendly** - Clean URLs and proper meta tags  
✅ **Admin Dashboard** - User management interface  
✅ **Error Handling** - Custom 404/500 pages  
✅ **Production Ready** - Deployment configuration included  

The platform successfully replicates the core functionalities of liveaevi.com while maintaining the original frontend design and adding a robust Flask backend for scalability and management.