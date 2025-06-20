from flask import Blueprint, jsonify, request, session
from app import db
from app.models import CartItem, Product
from flask_login import current_user
import uuid

bp = Blueprint('cart', __name__, url_prefix='/api/cart')


@bp.route('/', methods=['GET'])
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


@bp.route('/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    size = data.get('size')

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if current_user.is_authenticated:
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
        if 'cart_session_id' not in session:
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


@bp.route('/remove/<int:item_id>', methods=['DELETE'])
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


@bp.route('/update/<int:item_id>', methods=['PUT'])
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