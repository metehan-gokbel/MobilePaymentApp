from flask import jsonify, Blueprint, request, abort
from flask_jwt_extended import jwt_required
from ..models.wallet import Wallet

bp = Blueprint("wallet", __name__)


@bp.route('/get_wallet', methods=['POST'])
@jwt_required()
def get_wallet_data():
    data = request.get_json()
    if data != {}:
        response_data = Wallet.get_wallet_data(data['phone_number'])
        return jsonify(response_data)
    return {}


@bp.route('/deposit_money', methods=['PATCH'])  # REQUEST CONTENT: phone_number, tl
@jwt_required()
def update_wallet_data():
    data = request.get_json()
    response_data = Wallet.deposit_money(phone_number=data['phone_number'], tl=data['tl'])
    return jsonify(response_data)


@bp.route('/exchange', methods=['PATCH'])  # REQUEST CONTENT: phone_number, optionals: tl or mock_token
@jwt_required()
def exchange():
    data = request.get_json()
    balance_availability = Wallet.get_wallet_data(data['phone_number'])
    if 'tl' in data:
        if balance_availability['tl'] >= data['tl']:
            response_data = Wallet.exchange_to_mock(phone_number=data['phone_number'], tl=data['tl'])
            return jsonify(response_data)
        return abort(406)  # Insufficient balance
    elif 'mock_token' in data:
        if balance_availability['mock_token'] >= data['mock_token']:
            response_data = Wallet.exchange_to_tl(phone_number=data['phone_number'], mock_token=data['mock_token'])
            return jsonify(response_data)
        return abort(406)  # Insufficient balance
    return abort(400)
