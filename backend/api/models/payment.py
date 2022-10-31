from datetime import datetime
import os
from backend.api.db_connection.db_table import session, FuelingTable, PlateTable, TransactionTable

listener_api_url = os.getenv('LISTENER_API_URL')
verify_value = bool(os.getenv('verify_value'))


class Payment(dict):
    def __init__(self, **kwargs):
        print(kwargs)
        for key, value in kwargs.items():
            if key == 'acquirer_id':
                self.acquirer_id = kwargs.get('acquirer_id')
            elif key == 'bank_reference_number':
                self.bank_reference_number = kwargs.get('bank_reference_number')
            elif key == 'credit_card_number':
                self.credit_card_number = kwargs.get('credit_card_number')
            elif key == 'customer_license_plate':
                self.customer_license_plate = kwargs.get('customer_license_plate')
            elif key == 'fiscal_number':
                self.fiscal_number = kwargs.get('fiscal_number')
            elif key == 'fuel_type':
                self.fuel_type = kwargs.get('fuel_type')
            elif key == 'island_number':
                self.island_number = kwargs.get('island_number')
            elif key == 'liter':
                self.liter = kwargs.get('liter')
            elif key == 'paid_amount':
                self.paid_amount = kwargs.get('paid_amount')
            elif key == 'payment_id':
                self.payment_id = kwargs.get('payment_id')
            elif key == 'pump_number':
                self.pump_number = kwargs.get('pump_number')
            elif key == 'sale_id':
                self.sale_id = kwargs.get('sale_id')
            elif key == 'slip_text':
                self.slip_text = kwargs.get('slip_text')
            elif key == 'transaction_date_time':
                self.transaction_date_time = kwargs.get('transaction_date_time')
            elif key == 'unit_amount':
                self.unit_amount = kwargs.get('unit_amount')
            elif key == 'phone_number':
                self.phone_number = kwargs.get('phone_number')
        super().__init__(**kwargs)

    @classmethod
    def pay(cls, **data):
        data_id_request = session.query(PlateTable).filter_by(
            customer_license_plate=data['customer_license_plate']).first()
        if data_id_request is not None:
            fkPlateId = data_id_request.id
            data['fkPlateId'] = fkPlateId
            new_wallet = TransactionTable(**data)
            session.add(new_wallet)
            session.commit()
            return True
        return False

    @classmethod
    def get_to_pay(cls, customer_license_plate):
        fueling_to_pay = session.query(FuelingTable).filter_by(customer_license_plate=customer_license_plate).all()
        if fueling_to_pay is not None:
            result = []
            for fueling in fueling_to_pay:
                fueling_dict = fueling.to_dict()
                fueling_dict['paid_amount'] = float(fueling.to_dict()['paid_amount'])
                fueling_dict['unit_amount'] = float(fueling.to_dict()['unit_amount'])
                fueling_dict['liter'] = float(fueling.to_dict()['liter'])
                fueling_dict['island_number'] = float(fueling.to_dict()['island_number'])
                fueling_dict['transaction_date_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                del fueling_dict['fkPlateId']
                del fueling_dict['device_error_code']
                del fueling_dict['device_serial_number']
                del fueling_dict['device_version']
                result.append(fueling_dict)
            return result
        return []

    @classmethod
    def delete_paid_payment(cls, customer_license_plate):
        delete_plate = session.query(FuelingTable).filter_by(customer_license_plate=customer_license_plate).delete()
        if delete_plate == 1:
            session.commit()
            return True
        return False
