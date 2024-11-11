from flask import Blueprint, request, jsonify

from main_service.produce import send_to_exchange
from models import UserModel
from models import InventoryModel


buy_bp = Blueprint('buy_bp', __name__)

@buy_bp.route('/buy', methods=['POST'])
def buy():
    item_id = request.json.get('item_id')
    amount = request.json.get('amount')
    email = request.json.get('email')
    # validate that the user exists
    user = UserModel.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # validate that the item exists, and there is enough amount
    if not item_id:
        return jsonify({'error': 'Item ID is required'}), 400

    item = InventoryModel.query.filter_by(id=item_id).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    if item.amount < amount:
        return jsonify({'error': 'Not enough items in stock'}), 400
    # buy the item
    send_to_exchange(request.json)
    return jsonify({'message': 'Item bought'}), 200