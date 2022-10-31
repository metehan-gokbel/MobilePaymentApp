import requests
import os
from backend.api.db_connection.db_table import session, UserTable, PlateTable

listener_api_url = os.getenv('LISTENER_API_URL')
verify_value = bool(os.getenv('verify_value'))


class Plate(dict):
    def __init__(self, customer_license_plate, phone_number):
        self.customer_license_plate = customer_license_plate
        self.phone_number = phone_number
        super().__init__(customer_license_plate=self.customer_license_plate, phone_number=self.phone_number)

    @classmethod
    def add_plate(cls, phone_number, customer_license_plate):
        data_id_request = session.query(UserTable).filter_by(phone_number=phone_number).first()
        if data_id_request is not None:
            fkUserId = data_id_request.id
            new_wallet = PlateTable(phone_number=phone_number, customer_license_plate=customer_license_plate,
                                    fkUserId=fkUserId)
            session.add(new_wallet)
            session.commit()
            return True
        return False

    @classmethod
    def get_plates(cls, phone_number):
        get_all_plates_response = session.query(PlateTable).filter_by(phone_number=phone_number).all()
        if get_all_plates_response is not None:
            result = []
            for plate in get_all_plates_response:
                plate_dict = plate.to_dict()
                result.append(plate_dict['customer_license_plate'])
            return result
        return []

    @classmethod
    def payment_history(cls, customer_license_plate):
        plate_payment_history_response = requests.post(f"{listener_api_url}/plate_payment_history",
                                                       json={"customer_license_plate": customer_license_plate},
                                                       verify=verify_value)
        return plate_payment_history_response.json()

    @classmethod
    def del_plate(cls, phone_number, customer_license_plate):
        delete_plate = session.query(PlateTable).filter_by(customer_license_plate=customer_license_plate).delete()
        if delete_plate == 1:
            session.commit()
            return True
        return False
