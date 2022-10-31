from flask import jsonify, Blueprint, request, abort
from flask_jwt_extended import jwt_required
from ..models.wallet import Wallet
from ..models.user import User
from ..controllers import user_controller

bp = Blueprint("user", __name__)


@bp.route('/register', methods=['POST'])  # REQUEST CONTENT: phone_number, password
def register():
    data = request.get_json()
    registration_response = user_controller.registration_control(data)
    if registration_response is True:
        create_wallet = Wallet.create_wallet(data['phone_number'])
        if create_wallet is True:
            return jsonify(200)
    return abort(409)


@bp.route("/login", methods=["POST"])  # REQUEST CONTENT: phone_number, password, token_password
def login():
    data = request.get_json()
    response_data = user_controller.login_control(data)
    return jsonify(response_data[0]), response_data[1]


@bp.route('/update_password', methods=['PATCH'])  # REQUEST CONTENT: phone_number, new_password
@jwt_required()
def change_password():
    data = request.get_json()
    update_password_response = User.update_password(**data)
    if update_password_response is True:
        return jsonify(200)
    return abort(400)
