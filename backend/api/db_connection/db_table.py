from sqlalchemy import Column, Integer, String, Float, DateTime
from . import Base
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import bson

from . import Session

session = Session()


class UserTable(Base, SerializerMixin):
    __tablename__ = 'User'
    id = Column(String, primary_key=True)
    password = Column(String(512))
    phone_number = Column(String(24), unique=True)
    created_date = Column(DateTime, default=datetime.now())

    def __init__(self, id, password, phone_number):
        self.id = id
        self.password = password
        self.phone_number = phone_number


class PlateTable(Base, SerializerMixin):
    __tablename__ = 'Plate'
    id = Column(String, primary_key=True, default=str(bson.objectid.ObjectId()))
    fkUserId = Column(String, primary_key=True)
    phone_number = Column(String(512))
    customer_license_plate = Column(String(24), unique=True)
    created_date = Column(DateTime, default=datetime.now())

    def __init__(self, fkUserId, phone_number, customer_license_plate):
        self.fkUserId = fkUserId
        self.phone_number = phone_number
        self.customer_license_plate = customer_license_plate


class WalletTable(Base, SerializerMixin):
    __tablename__ = 'Wallet'
    id = Column(String, primary_key=True, default=str(bson.objectid.ObjectId()))
    fkUserId = Column(String)
    phone_number = Column(String(512))
    mock_token = Column(Float(24), default=0)
    tl = Column(Float(24), default=0)
    mock_token_to_tl = Column(Float(24), default=0)
    tl_to_mock_token = Column(Float(24), default=0)
    total = Column(Float(24), default=0)
    created_date = Column(DateTime, default=datetime.now())

    def __init__(self, fkUserId, phone_number, mock_token, tl, mock_token_to_tl, tl_to_mock_token, total):
        self.fkUserId = fkUserId
        self.phone_number = phone_number
        self.mock_token = mock_token
        self.tl = tl
        self.tl_to_mock_token = tl_to_mock_token
        self.mock_token_to_tl = mock_token_to_tl
        self.total = total


class TransactionTable(Base, SerializerMixin):
    __tablename__ = 'Transaction'
    id = Column(String, primary_key=True, default=str(bson.objectid.ObjectId()))
    fkPlateId = Column(String)
    created_date = Column(DateTime, default=datetime.now())

    def __init__(self, **kwargs):
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
            elif key == 'fkPlateId':
                self.fkPlateId = kwargs.get('fkPlateId')


class FuelingTable(Base, SerializerMixin):
    __tablename__ = 'Fueling'
    id = Column(String, primary_key=True, default=str(bson.objectid.ObjectId()))
    fkPlateId = Column(String, primary_key=True)
    device_serial_number = Column(String(512))
    device_version = Column(String(512))
    device_error_code = Column(Integer)
    customer_license_plate = Column(String(512))
    fiscal_number = Column(String(512))
    fuel_type = Column(String(512))
    island_number = Column(String(512))
    liter = Column(String(512))
    paid_amount = Column(String(512))
    pump_number = Column(Integer)
    sale_id = Column(Integer, autoincrement=True)
    payment_id = Column(Integer)
    unit_amount = Column(Float(24))
    created_date = Column(DateTime, default=datetime.now())

    def __init__(self, fkPlateId, customer_license_plate, device_serial_number, device_version, device_error_code,
                 fiscal_number, fuel_type, island_number, liter, paid_amount, payment_id, pump_number, sale_id,
                 unit_amount):
        self.fkPlateId = fkPlateId
        self.device_serial_number = device_serial_number
        self.device_version = device_version
        self.device_error_code = device_error_code
        self.customer_license_plate = customer_license_plate
        self.fiscal_number = fiscal_number
        self.fuel_type = fuel_type
        self.island_number = island_number
        self.liter = liter
        self.paid_amount = paid_amount
        self.payment_id = payment_id
        self.pump_number = pump_number
        self.sale_id = sale_id
        self.unit_amount = unit_amount
