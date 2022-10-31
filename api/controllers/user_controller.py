import hashlib
from datetime import datetime
import bson
from flask import abort
from flask_jwt_extended import create_access_token
from ..db_connection.db_table import session, UserTable
from ..models.user import User


def registration_control(data):
    try:
        new_user = User(**data)
    except Exception as e:
        return {'message': e}, 400
    unique_control = session.query(UserTable).filter_by(phone_number=new_user.phone_number).first()
    if not unique_control:
        url = UserTable(id=str(bson.objectid.ObjectId()),
                        phone_number=new_user.phone_number,
                        password=hashlib.md5(new_user.password.encode()).hexdigest())
        session.add(url)
        session.commit()
        session.close()
        return True
    return False


def login_control(data):
    try:
        new_user = User(phone_number=data['phone_number'], password=data['password'],
                        token_password=data['token_password'])
    except Exception as e:
        return {'message': e}, 400
    unique_control = session.query(UserTable).filter_by(phone_number=new_user.phone_number,
                                                        password=new_user.password).first()
    if unique_control and new_user.token_password == datetime.now().strftime('%d.%m.%Y %H'):
        access_token = create_access_token(identity=data)
        data['access_token'] = access_token
        return {'access_token': data.pop('access_token')}, 200
    return {}, abort(401)
