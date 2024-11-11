from flask import Blueprint, request, jsonify

from models import UserModel
from database import db_session

signup_bp = Blueprint('signup_bp', __name__)


@signup_bp.route('/sign_up', methods=['POST'])
def sign_up():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = UserModel(email=email)
    try:
        db_session.add(user)
        db_session.commit()
        return jsonify({
            'id': user.id,
            'message': 'User created'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
