from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db

bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/profile')
@login_required
def get_user_profile():
    """Get current user profile"""
    return jsonify(current_user.to_dict())


@bp.route('/profile', methods=['PUT'])
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