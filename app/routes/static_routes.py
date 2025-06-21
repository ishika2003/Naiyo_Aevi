from flask import Blueprint, render_template
from app.models import CartItem, Product
from flask_login import current_user
from flask import session

bp = Blueprint('static', __name__)


@bp.route('/')
def home():
    """Serve the homepage unchanged"""
    return render_template('index.html')


@bp.route('/about')
def about():
    """About page route"""
    return render_template('about.html')


@bp.route('/shop')
def shop():
    """Shop page route"""
    return render_template('shop.html')


@bp.route('/contact')
def contact():
    """Contact page route"""
    return render_template('contact.html')


@bp.route('/blog')
def blog():
    """Blog/Journal page route"""
    return render_template('blog.html')


@bp.route('/single-post')
def single_post():
    """Single post page route"""
    return render_template('single-post.html')


@bp.route('/thank-you')
def thank_you():
    """Thank you page route"""
    return render_template('thank-you.html')


@bp.route('/cart')
def cart():
    """Shopping cart page"""
    cart_items = []
    cart_total = 0

    if current_user.is_authenticated:
        cart_items_db = CartItem.query.filter_by(user_id=current_user.id).all()
    else:
        session_id = session.get('cart_session_id')
        if session_id:
            cart_items_db = CartItem.query.filter_by(session_id=session_id).all()
        else:
            cart_items_db = []

    for item in cart_items_db:
        item_total = item.product.price * item.quantity
        cart_total += item_total
        cart_items.append({
            'item': item,
            'product': item.product,
            'item_total': item_total
        })

    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)


@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Dynamic product detail page"""
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()

    return render_template('product-detail.html', product=product, related_products=related_products)


@bp.route('/category/<category_name>')
def category_products(category_name):
    """Products by category"""
    products = Product.query.filter_by(category=category_name).all()
    return render_template('category.html', products=products, category=category_name)