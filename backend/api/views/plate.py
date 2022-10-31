from flask import jsonify, Blueprint, request, abort
from flask_jwt_extended import jwt_required
from backend.api.models.plate import Plate

bp = Blueprint("plate", __name__)


@bp.route('/add_plate', methods=['POST'])  # REQUEST CONTENT: phone_number, customer_license_plate
@jwt_required()
def add_plates_view():
    data = request.get_json()
    response = Plate.add_plate(phone_number=data['phone_number'],
                               customer_license_plate=data['customer_license_plate'])
    if response is True:
        return jsonify(200)
    return jsonify(400)


@bp.route('/get_plate', methods=['POST'])  # REQUEST CONTENT: phone_number
@jwt_required()
def get_all_plates():
    data = request.get_json()
    response = Plate.get_plates(phone_number=data['phone_number'])
    return jsonify(response)


@bp.route('/plate_payment_history', methods=['POST'])  # REQUEST CONTENT: phone_number, customer_license_plate
@jwt_required()
def plate_payment_history():
    data = request.get_json()
    response = Plate.payment_history(customer_license_plate=data['customer_license_plate'])
    return jsonify(response)


@bp.route('/delete_plate', methods=['POST'])  # REQUEST CONTENT: phone_number, customer_license_plate
@jwt_required()
def delete_plate():
    data = request.get_json()
    response = Plate.del_plate(phone_number=data['phone_number'],
                               customer_license_plate=data['customer_license_plate'])
    if response is True:
        return jsonify(200)
    return abort(400)
