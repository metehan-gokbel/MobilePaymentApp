from sqlalchemy import func
from api.db_connection.db_table import session, FuelingTable

new_payment = {
    "customer_license_plate": "22NA300",
    "device_error_code": 0,
    "fkPlateId": "1",
    "unit_amount": 15.2,
    "device_serial_number": "mockSerialNumber",
    "device_version": "1.1.1",
    "fiscal_number": "mockFiscalNumber",
    "island_number": 1,
    "liter": 5.0,
    "paid_amount": 30.0,
    "fuel_type": "Diesel",
    "pump_number": 1,
    "sale_id": 1,
    "payment_id": 1
}


def payment_ready_to_pay(new_payment):
    unique_control = session.query(func.max(FuelingTable.sale_id)).first()
    if unique_control[0] is None or new_payment['sale_id'] > unique_control[0]:
        fueling = FuelingTable(customer_license_plate=new_payment["customer_license_plate"],
                               device_error_code=new_payment["device_error_code"],
                               fkPlateId=new_payment["fkPlateId"],
                               unit_amount=new_payment["unit_amount"],
                               device_serial_number=new_payment["device_serial_number"],
                               device_version=new_payment["device_version"],
                               fiscal_number=new_payment["fiscal_number"],
                               island_number=new_payment["island_number"],
                               liter=new_payment["liter"],
                               paid_amount=new_payment["paid_amount"],
                               fuel_type=new_payment["fuel_type"],
                               pump_number=new_payment["pump_number"],
                               sale_id=new_payment["sale_id"],
                               payment_id=new_payment["payment_id"])

        session.add(fueling)
        session.commit()
        return True, "--- Mock Payment Added to DB!"
    return False, "--- Sale Id already exists!"


if __name__ == '__main__':
    a = payment_ready_to_pay(new_payment)
    print(*a)
