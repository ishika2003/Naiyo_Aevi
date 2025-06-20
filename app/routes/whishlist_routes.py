from flask import Blueprint, jsonify, request
from app import db
from app.models import Wishlist, Product
from flask_login import login_required, current_user

bp = Blueprint('wishlist', __name__, url_prefix='/api/wishlist')


@bp.route('/', methods=['GET'])
@login_required
def get_wishlist():
    """Get user's wishlist"""
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return jsonify([item.to_dict() for item in wishlist_items])


@bp.route('/add', methods=['POST'])
@login_required
def add_to_wishlist():
    """Add item to wishlist"""
    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    existing_item = Wishlist.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if existing_item:
        return jsonify({'error': 'Item already in wishlist'}), 400

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


@bp.route('/remove/<int:product_id>', methods=['DELETE'])
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