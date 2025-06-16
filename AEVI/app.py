from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///aevi.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'
CORS(app)

# Database Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_subscribed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_subscribed': self.is_subscribed,
            'created_at': self.created_at.isoformat()
        }

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    subject = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'phone': self.phone,
            'subject': self.subject,
            'created_at': self.created_at.isoformat()
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    image_main = db.Column(db.String(500), nullable=True)
    image_hover = db.Column(db.String(500), nullable=True)
    is_bestseller = db.Column(db.Boolean, default=False)
    is_new = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    in_stock = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Enhanced fields for liveaevi.com functionality
    short_description = db.Column(db.String(500), nullable=True)  # For card descriptions
    ingredients = db.Column(db.Text, nullable=True)  # Product ingredients
    how_to_use = db.Column(db.Text, nullable=True)  # Usage instructions
    benefits = db.Column(db.Text, nullable=True)  # Product benefits
    size_options = db.Column(db.Text, nullable=True)  # JSON string for sizes like "50ml, 250ml"
    tags = db.Column(db.Text, nullable=True)  # Comma-separated tags
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'short_description': self.short_description,
            'price': self.price,
            'category': self.category,
            'image_main': self.image_main,
            'image_hover': self.image_hover,
            'is_bestseller': self.is_bestseller,
            'is_new': self.is_new,
            'rating': self.rating,
            'review_count': self.review_count,
            'in_stock': self.in_stock,
            'ingredients': self.ingredients,
            'how_to_use': self.how_to_use,
            'benefits': self.benefits,
            'size_options': self.size_options,
            'tags': self.tags,
            'created_at': self.created_at.isoformat()
        }

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # For logged-in users
    session_id = db.Column(db.String(100), nullable=True)  # For anonymous users
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    size = db.Column(db.String(50), nullable=True)  # For products with size options
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='cart_items')
    user = db.relationship('User', backref='cart_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'size': self.size,
            'created_at': self.created_at.isoformat()
        }

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='wishlist_items')
    user = db.relationship('User', backref='wishlist_items')
    
    # Ensure unique wishlist items per user
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_wishlist'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict() if self.product else None,
            'created_at': self.created_at.isoformat()
        }

class Newsletter(db.Model):
    __tablename__ = 'newsletter'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'subscribed_at': self.subscribed_at.isoformat(),
            'is_active': self.is_active
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes - Serve static pages
@app.route('/')
def home():
    """Serve the homepage unchanged"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/shop')
def shop():
    """Shop page route"""
    return render_template('shop.html')

@app.route('/contact')
def contact():
    """Contact page route"""
    return render_template('contact.html')

@app.route('/blog')
def blog():
    """Blog/Journal page route"""
    return render_template('blog.html')

@app.route('/single-post')
def single_post():
    """Single post page route"""
    return render_template('single-post.html')

@app.route('/thank-you')
def thank_you():
    """Thank you page route"""
    return render_template('thank-you.html')

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart_items = []
    cart_total = 0
    
    if current_user.is_authenticated:
        # Get cart for logged-in user
        cart_items_db = CartItem.query.filter_by(user_id=current_user.id).all()
    else:
        # Get cart for anonymous session
        session_id = session.get('cart_session_id')
        if session_id:
            cart_items_db = CartItem.query.filter_by(session_id=session_id).all()
        else:
            cart_items_db = []
    
    # Calculate total and prepare cart items
    for item in cart_items_db:
        item_total = item.product.price * item.quantity
        cart_total += item_total
        cart_items.append({
            'item': item,
            'product': item.product,
            'item_total': item_total
        })
    
    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)

# Dynamic routes
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Dynamic product detail page"""
    product = Product.query.get_or_404(product_id)
    # Get related products (same category)
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()
    
    return render_template('product-detail.html', product=product, related_products=related_products)

@app.route('/category/<category_name>')
def category_products(category_name):
    """Products by category"""
    products = Product.query.filter_by(category=category_name).all()
    return render_template('category.html', products=products, category=category_name)

# API Routes
@app.route('/api/products')
def get_products():
    """Get all products"""
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/products/bestsellers')
def get_bestsellers():
    """Get bestseller products"""
    products = Product.query.filter_by(is_bestseller=True).all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/products/new')
def get_new_products():
    """Get new products"""
    products = Product.query.filter_by(is_new=True).all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/products/category/<category>')
def get_products_by_category(category):
    """Get products by category"""
    products = Product.query.filter_by(category=category).all()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/search')
def search_products():
    """Search products by name, description, or tags"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    
    # Search in name, description, short_description, and tags
    search_term = f'%{query}%'
    products = Product.query.filter(
        db.or_(
            Product.name.ilike(search_term),
            Product.description.ilike(search_term),
            Product.short_description.ilike(search_term),
            Product.tags.ilike(search_term)
        )
    ).limit(20).all()
    
    return jsonify([product.to_dict() for product in products])

# Enhanced API Routes for filtering and sorting
@app.route('/api/products/filter')
def filter_products():
    """Filter products with enhanced options"""
    category = request.args.get('category')
    sort_by = request.args.get('sort', 'name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock = request.args.get('in_stock', type=bool)
    
    query = Product.query
    
    # Apply filters
    if category and category != 'all':
        if category == 'bestsellers':
            query = query.filter_by(is_bestseller=True)
        elif category == 'new-in':
            query = query.filter_by(is_new=True)
        else:
            # Convert category filter format (e.g., 'cleansers-masks' to 'Cleansers & Masks')
            category_formatted = category.replace('-', ' & ').title()
            query = query.filter(Product.category.ilike(f'%{category_formatted}%'))
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    if in_stock is not None:
        query = query.filter_by(in_stock=in_stock)
    
    # Apply sorting
    if sort_by == 'price-low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price-high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.name.asc())
    
    products = query.all()
    return jsonify([product.to_dict() for product in products])

# Cart Management Routes
@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get cart items for current user or session"""
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    else:
        session_id = session.get('cart_session_id')
        if not session_id:
            return jsonify([])
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
    
    return jsonify([item.to_dict() for item in cart_items])

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    size = data.get('size')
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    # Verify product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if current_user.is_authenticated:
        # For logged-in users
        existing_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id,
            size=size
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity,
                size=size
            )
            db.session.add(cart_item)
    else:
        # For anonymous users
        if 'cart_session_id' not in session:
            import uuid
            session['cart_session_id'] = str(uuid.uuid4())
        
        session_id = session['cart_session_id']
        existing_item = CartItem.query.filter_by(
            session_id=session_id,
            product_id=product_id,
            size=size
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            cart_item = CartItem(
                session_id=session_id,
                product_id=product_id,
                quantity=quantity,
                size=size
            )
            db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Item added to cart'})

@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    """Remove item from cart"""
    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    else:
        session_id = session.get('cart_session_id')
        cart_item = CartItem.query.filter_by(id=item_id, session_id=session_id).first()
    
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Item removed from cart'})

@app.route('/api/cart/update/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    """Update cart item quantity"""
    data = request.get_json()
    quantity = data.get('quantity', 1)
    
    if quantity < 1:
        return jsonify({'error': 'Quantity must be at least 1'}), 400
    
    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    else:
        session_id = session.get('cart_session_id')
        cart_item = CartItem.query.filter_by(id=item_id, session_id=session_id).first()
    
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    cart_item.quantity = quantity
    db.session.commit()
    return jsonify({'success': True, 'message': 'Cart updated'})

# Wishlist Management Routes
@app.route('/api/wishlist', methods=['GET'])
@login_required
def get_wishlist():
    """Get user's wishlist"""
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return jsonify([item.to_dict() for item in wishlist_items])

@app.route('/api/wishlist/add', methods=['POST'])
@login_required
def add_to_wishlist():
    """Add item to wishlist"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    # Check if already in wishlist
    existing_item = Wishlist.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if existing_item:
        return jsonify({'error': 'Item already in wishlist'}), 400
    
    # Verify product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    wishlist_item = Wishlist(
        user_id=current_user.id,
        product_id=product_id
    )
    
    db.session.add(wishlist_item)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Item added to wishlist'})

@app.route('/api/wishlist/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_wishlist(product_id):
    """Remove item from wishlist"""
    wishlist_item = Wishlist.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if not wishlist_item:
        return jsonify({'error': 'Item not found in wishlist'}), 404
    
    db.session.delete(wishlist_item)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Item removed from wishlist'})

# Authentication routes
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """User sign in"""
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if request.is_json:
                return jsonify({'success': True, 'user': user.to_dict()})
            else:
                flash('Successfully signed in!', 'success')
                return redirect(url_for('home'))
        else:
            if request.is_json:
                return jsonify({'error': 'Invalid credentials'}), 401
            else:
                flash('Invalid email or password', 'error')
                return render_template('signin.html')
    
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign up"""
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            first_name = request.form.get('first_name', '')
            last_name = request.form.get('last_name', '')
        
        if User.query.filter_by(email=email).first():
            if request.is_json:
                return jsonify({'error': 'Email already exists'}), 400
            else:
                flash('Email already registered', 'error')
                return render_template('signup.html')
        
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        
        if request.is_json:
            return jsonify({'success': True, 'user': user.to_dict()})
        else:
            flash('Account created successfully!', 'success')
            return redirect(url_for('home'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html', user=current_user)

# Form submission routes
@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission"""
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        phone = data.get('phone', '')
        subject = data.get('subject', '')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        phone = request.form.get('phone', '')
        subject = request.form.get('subject', '')
    
    # Save to database
    lead = Lead(
        name=name,
        email=email,
        message=message,
        phone=phone,
        subject=subject
    )
    
    db.session.add(lead)
    db.session.commit()
    
    # Send email notification
    try:
        msg = Message(
            subject=f'New Contact Form Submission: {subject}',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f'''
            New contact form submission:
            
            Name: {name}
            Email: {email}
            Phone: {phone}
            Subject: {subject}
            
            Message:
            {message}
            '''
        )
        mail.send(msg)
    except Exception as e:
        app.logger.error(f'Failed to send email: {e}')
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Thank you for your message!'})
    else:
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('thank_you'))

@app.route('/subscribe-newsletter', methods=['POST'])
def subscribe_newsletter():
    """Handle newsletter subscription"""
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
    else:
        email = request.form.get('email')
    
    if not email:
        if request.is_json:
            return jsonify({'error': 'Email is required'}), 400
        else:
            flash('Email is required', 'error')
            return redirect(url_for('home'))
    
    # Check if already subscribed
    existing = Newsletter.query.filter_by(email=email).first()
    if existing:
        if request.is_json:
            return jsonify({'message': 'Already subscribed!'})
        else:
            flash('You are already subscribed to our newsletter!', 'info')
            return redirect(url_for('home'))
    
    # Add to newsletter
    newsletter = Newsletter(email=email)
    db.session.add(newsletter)
    
    # Update user subscription status if user exists
    user = User.query.filter_by(email=email).first()
    if user:
        user.is_subscribed = True
    
    db.session.commit()
    
    # Send welcome email
    try:
        msg = Message(
            subject='Welcome to AEVI Newsletter!',
            sender=app.config['MAIL_USERNAME'],
            recipients=[email],
            body='''
            Welcome to AEVI!
            
            Thank you for subscribing to our newsletter. 
            You'll receive exclusive updates about our Nordic skincare products.
            
            Enjoy 10% off your first order!
            
            Best regards,
            The AEVI Team
            '''
        )
        mail.send(msg)
    except Exception as e:
        app.logger.error(f'Failed to send welcome email: {e}')
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Successfully subscribed!'})
    else:
        flash('Successfully subscribed to our newsletter!', 'success')
        return redirect(url_for('home'))

# Protected routes

@app.route('/api/user/profile')
@login_required
def get_user_profile():
    """Get current user profile"""
    return jsonify(current_user.to_dict())

@app.route('/api/user/profile', methods=['PUT'])
@login_required
def update_user_profile():
    """Update user profile"""
    data = request.get_json()
    
    if 'first_name' in data:
        current_user.first_name = data['first_name']
    if 'last_name' in data:
        current_user.last_name = data['last_name']
    
    db.session.commit()
    
    return jsonify({'success': True, 'user': current_user.to_dict()})

# Additional API endpoints

@app.route('/api/newsletter/unsubscribe', methods=['POST'])
def unsubscribe_newsletter():
    """Unsubscribe from newsletter"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Deactivate newsletter subscription
    newsletter = Newsletter.query.filter_by(email=email).first()
    if newsletter:
        newsletter.is_active = False
        db.session.commit()
    
    # Update user subscription status
    user = User.query.filter_by(email=email).first()
    if user:
        user.is_subscribed = False
        db.session.commit()
    
    return jsonify({'success': True, 'message': 'Successfully unsubscribed from newsletter'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Initialize database
def generate_stars(rating):
    """Generate star rating display"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = '★' * full_stars
    if half_star:
        stars += '☆'
    # stars += '☆' * empty_stars
    
    return stars

# Make the function available in templates
app.jinja_env.globals.update(generate_stars=generate_stars)

def init_db():
    """Initialize database with tables and sample data"""
    db.create_all()
    
    # Add sample products if none exist
    if Product.query.count() == 0:
        sample_products = [
            Product(
                name='NOURISHING FACE OIL',
                description='A luxurious face oil that deeply nourishes and restores radiance to tired, dull skin. Formulated with potent Nordic super berries rich in antioxidants and vitamins.',
                short_description='Radiance Enhancing Nordic Super Berries',
                price=98.00,
                category='serums-oils',
                image_main='static/images/nourishing-face-oil.jpg',
                image_hover='static/images/nourishing-face-oil.jpg',
                is_bestseller=True,
                rating=4.9,
                review_count=20,
                ingredients='Sea Buckthorn Oil, Cloudberry Seed Oil, Lingonberry Extract, Rosehip Oil, Vitamin E',
                how_to_use='Apply 2-3 drops to clean skin morning and evening. Gently massage until absorbed.',
                benefits='Brightens skin, reduces fine lines, improves elasticity, provides deep hydration',
                size_options='30ml',
                tags='bestseller,face oil,anti-aging,radiance,nordic berries'
            ),
            Product(
                name='HYALURONIC ACID FACE SERUM',
                description='An intensely hydrating serum that plumps and smooths skin with multiple molecular weights of hyaluronic acid, enhanced with Nordic seaweed extracts.',
                short_description='Super Hydrating Seaweed + Tremella',
                price=94.00,
                category='serums-oils',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                is_bestseller=True,
                rating=4.8,
                review_count=15,
                ingredients='Hyaluronic Acid (3 molecular weights), Tremella Mushroom Extract, Nordic Seaweed, Aloe Vera',
                how_to_use='Apply to clean skin before moisturizer, morning and evening.',
                benefits='Intense hydration, plumps fine lines, improves skin texture, long-lasting moisture',
                size_options='30ml',
                tags='bestseller,hyaluronic acid,hydration,serum,plumping'
            ),
            Product(
                name='ALL-OVER BALM',
                description='A multi-purpose healing balm that soothes, protects, and nourishes skin anywhere you need it. Perfect for dry patches, cuticles, and sensitive areas.',
                short_description='Everywhere Essential',
                price=24.00,
                category='balms',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                is_bestseller=True,
                rating=4.7,
                review_count=10,
                ingredients='Shea Butter, Coconut Oil, Beeswax, Calendula Extract, Chamomile Oil',
                how_to_use='Apply to dry or irritated skin as needed. Safe for face and body.',
                benefits='Soothes irritation, protects skin barrier, deeply moisturizes, versatile use',
                size_options='15ml',
                tags='bestseller,balm,healing,multi-purpose,sensitive skin'
            ),
            Product(
                name='CLARIFYING CLAY MASK',
                description='A powerful detoxifying mask formulated with natural Nordic blue clays that draw out impurities while gently exfoliating for clearer, smoother skin.',
                short_description='Detoxifying Natural Blue Clays',
                price=38.00,
                category='cleansers-masks',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                is_new=True,
                rating=4.6,
                review_count=8,
                ingredients='Nordic Blue Clay, Kaolin Clay, Charcoal Powder, Tea Tree Oil, Witch Hazel',
                how_to_use='Apply even layer to clean skin, avoid eye area. Leave for 10-15 minutes, rinse with warm water.',
                benefits='Deep cleanses pores, removes impurities, controls oil, improves skin texture',
                size_options='75ml',
                tags='new,clay mask,detox,pore care,deep cleanse'
            ),
            Product(
                name='EYE ELIXIR',
                description='A gentle yet effective eye treatment that brightens dark circles and reduces puffiness with awakening tea extracts and Nordic berries.',
                short_description='Awakening Tea Extracts + Brightening Berries',
                price=62.00,
                category='treatments',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                rating=4.5,
                review_count=12,
                ingredients='Green Tea Extract, Caffeine, Cloudberry Extract, Peptides, Niacinamide',
                how_to_use='Gently pat around eye area morning and evening using ring finger.',
                benefits='Reduces dark circles, minimizes puffiness, firms delicate skin, brightens eye area',
                size_options='15ml',
                tags='eye care,dark circles,puffiness,brightening,tea extracts'
            ),
            Product(
                name='LUMI BALM',
                description='A natural dewy highlighter that gives skin a subtle, healthy glow. Perfect for creating that effortless Nordic radiance.',
                short_description='Dewy Highlighter',
                price=28.00,
                category='balms',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                rating=4.4,
                review_count=6,
                ingredients='Coconut Oil, Mica, Jojoba Oil, Vitamin E, Natural Fragrance',
                how_to_use='Apply to high points of face: cheekbones, nose bridge, cupids bow.',
                benefits='Natural glow, buildable coverage, nourishing formula, long-lasting',
                size_options='8ml',
                tags='highlighter,glow,natural,radiance,makeup'
            ),
            Product(
                name='AWAKENING HAND & BODY WASH',
                description='An energizing cleansing gel infused with Nordic pine, eucalyptus, and frankincense to awaken your senses while gently cleansing.',
                short_description='Nordic Pine, Eucalyptus + Frankincense',
                price=15.00,
                category='body',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                rating=4.3,
                review_count=18,
                ingredients='Nordic Pine Extract, Eucalyptus Oil, Frankincense, Coconut-derived Cleansers',
                how_to_use='Apply to wet skin, lather, and rinse thoroughly. Use daily.',
                benefits='Gentle cleansing, energizing scent, natural ingredients, suitable for sensitive skin',
                size_options='50ml,250ml',
                tags='body wash,energizing,pine,eucalyptus,natural'
            ),
            Product(
                name='HYDRATING HAND & BODY LOTION',
                description='A deeply moisturizing lotion that absorbs quickly while providing long-lasting hydration with the same signature Nordic scent blend.',
                short_description='Nordic Pine, Eucalyptus + Frankincense',
                price=15.00,
                category='body',
                image_main='static/images/AEVI/Page1.webp',
                image_hover='static/images/AEVI/Page1.webp',
                rating=4.2,
                review_count=14,
                ingredients='Shea Butter, Coconut Oil, Nordic Pine Extract, Eucalyptus Oil, Frankincense',
                how_to_use='Apply to clean skin, massage until absorbed. Use daily or as needed.',
                benefits='Deep hydration, fast absorption, long-lasting moisture, signature scent',
                size_options='50ml,250ml',
                tags='body lotion,hydrating,fast absorbing,signature scent'
            )
        ]
        
        for product in sample_products:
            db.session.add(product)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)