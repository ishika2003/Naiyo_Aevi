from flask import Blueprint, jsonify, request
from app import db
from app.models import Product

bp = Blueprint('products', __name__, url_prefix='/api/products')


@bp.route('/')
def get_products():
    """Get all products"""
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])


@bp.route('/bestsellers')
def get_bestsellers():
    """Get bestseller products"""
    products = Product.query.filter_by(is_bestseller=True).all()
    return jsonify([product.to_dict() for product in products])


@bp.route('/new')
def get_new_products():
    """Get new products"""
    products = Product.query.filter_by(is_new=True).all()
    return jsonify([product.to_dict() for product in products])


@bp.route('/category/<category>')
def get_products_by_category(category):
    """Get products by category"""
    products = Product.query.filter_by(category=category).all()
    return jsonify([product.to_dict() for product in products])


@bp.route('/search')
def search_products():
    """Search products by name, description, or tags"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

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


@bp.route('/filter')
def filter_products():
    """Filter products with enhanced options"""
    category = request.args.get('category')
    sort_by = request.args.get('sort', 'name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock = request.args.get('in_stock', type=bool)

    query = Product.query

    if category and category != 'all':
        if category == 'bestsellers':
            query = query.filter_by(is_bestseller=True)
        elif category == 'new-in':
            query = query.filter_by(is_new=True)
        else:
            category_formatted = category.replace('-', ' & ').title()
            query = query.filter(Product.category.ilike(f'%{category_formatted}%'))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if in_stock is not None:
        query = query.filter_by(in_stock=in_stock)

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