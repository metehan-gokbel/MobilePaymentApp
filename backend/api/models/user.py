import hashlib
import os
from backend.api.db_connection.db_table import session, UserTable

listener_api_url = os.getenv('LISTENER_API_URL')
verify_value = bool(os.getenv('verify_value'))


class User(dict):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "phone_number":
                self.phone_number = kwargs.get("phone_number")
            elif key == "password":
                self.password = hashlib.md5(kwargs.get("password").encode()).hexdigest()
            elif key == "new_password":
                self.new_password = hashlib.md5(kwargs.get("new_password").encode()).hexdigest()
            elif key == "token_password":
                self.token_password = kwargs.get("token_password")
        super().__init__(**kwargs)

    @staticmethod
    def verify_new_password(password, new_password, re_new_password):
        if new_password == re_new_password and new_password != password:
            return True
        return False

    @classmethod
    def update_password(cls, **kwargs):
        phone_number = kwargs.get("phone_number")
        new_password = kwargs.get("new_password")

        update_password = session.query(UserTable).filter(phone_number == phone_number).one()
        update_password.password = hashlib.md5(new_password.encode()).hexdigest()
        session.commit()
        return True

