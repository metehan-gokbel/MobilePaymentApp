import os
from api.db_connection.db_table import session, UserTable, WalletTable

listener_api_url = os.getenv('LISTENER_API_URL')
verify_value = bool(os.getenv('verify_value'))


class Wallet(dict):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "mock_token":
                self["mock_token"] = kwargs.get("mock_token")
            elif key == "tl":
                self["tl"] = kwargs.get("tl")
            elif key == "mock_token_to_tl":
                self["mock_token_to_tl"] = kwargs.get("mock_token_to_tl")
            elif key == "total":
                self["total"] = kwargs.get("total")
            elif key == "phone_number":
                self["phone_number"] = kwargs.get("phone_number")
        super().__init__(**kwargs)

    @classmethod
    def create_wallet(cls, phone_number):  # REQUEST CONTENT: phone_number
        data_id_request = session.query(UserTable).filter_by(phone_number=phone_number).first()
        if data_id_request is not None:
            fkUserId = data_id_request.id
            new_wallet = WalletTable(phone_number=phone_number, fkUserId=fkUserId,
                                     tl=0, mock_token=0, total=0, mock_token_to_tl=0,
                                     tl_to_mock_token=0)
            session.add(new_wallet)
            session.commit()
            return True
        return False

    @classmethod
    def check_wallet_amount(cls, phone_number):
        current_wallet = session.query(WalletTable).filter_by(phone_number=phone_number).first()
        current_tl = current_wallet.tl
        return current_tl

    @classmethod
    def get_wallet_data(cls, phone_number):
        wallet_response = session.query(WalletTable).filter_by(phone_number=phone_number).first()
        if wallet_response is not None:
            result = wallet_response.to_dict()
            del result['id']
            del result['fkUserId']
            del result['created_date']
            return result
        return {}

    @classmethod
    def deposit_money(cls, phone_number, tl):
        user = session.query(UserTable).filter_by(phone_number=phone_number).first()
        fkUserId = user.id
        current_wallet = session.query(WalletTable).filter_by(phone_number=phone_number).first()
        if current_wallet is not None:
            current_tl = current_wallet.tl
            current_mock_token = current_wallet.mock_token

            tl = current_tl + tl
            mock_token = current_mock_token + (tl * 0.001)
            mock_token_to_tl = mock_token / 0.5
            total = tl + mock_token_to_tl

            new_wallet = session.query(WalletTable).filter(fkUserId == fkUserId).one()
            new_wallet.tl = tl
            new_wallet.mock_token = mock_token
            new_wallet.mock_token_to_tl = mock_token_to_tl
            new_wallet.tl_to_mock_token = current_wallet.tl_to_mock_token
            new_wallet.total = total
            session.commit()

            return {"tl": tl,
                    "mock_token": mock_token,
                    "mock_token_to_tl": mock_token_to_tl,
                    "total": total}
        return {}

    @classmethod
    def exchange_to_mock(cls, phone_number, tl):
        user = session.query(UserTable).filter_by(phone_number=phone_number).first()
        fkUserId = user.id
        current_wallet = session.query(WalletTable).filter_by(phone_number=phone_number).first()
        if current_wallet is not None:
            current_tl = current_wallet.tl
            current_mock_token = current_wallet.mock_token

            mock_token = current_mock_token + (tl * 0.5)
            mock_token_to_tl = mock_token / 0.5
            tl = current_tl - tl
            total = tl + mock_token_to_tl

            new_wallet = session.query(WalletTable).filter(fkUserId == fkUserId).one()
            new_wallet.tl = tl
            new_wallet.mock_token = mock_token
            new_wallet.mock_token_to_tl = mock_token_to_tl
            new_wallet.tl_to_mock_token = current_wallet.tl_to_mock_token
            new_wallet.total = total
            session.commit()

            return {"tl": tl,
                    "mock_token": mock_token,
                    "mock_token_to_tl": mock_token_to_tl,
                    "total": total}
        return {}

    @classmethod
    def exchange_to_tl(cls, phone_number, mock_token):
        user = session.query(UserTable).filter_by(phone_number=phone_number).first()
        fkUserId = user.id
        current_wallet = session.query(WalletTable).filter_by(phone_number=phone_number).first()
        if current_wallet is not None:
            current_tl = current_wallet.tl
            current_mock_token = current_wallet.mock_token

            tl = current_tl + (mock_token / 0.5)
            mock_token = current_mock_token - mock_token
            mock_token_to_tl = mock_token / 0.5
            total = tl + mock_token_to_tl

            new_wallet = session.query(WalletTable).filter(fkUserId == fkUserId).one()
            new_wallet.tl = tl
            new_wallet.mock_token = mock_token
            new_wallet.mock_token_to_tl = mock_token_to_tl
            new_wallet.tl_to_mock_token = current_wallet.tl_to_mock_token
            new_wallet.total = total
            session.commit()

            return {"tl": tl,
                    "mock_token": mock_token,
                    "mock_token_to_tl": mock_token_to_tl,
                    "total": total}
        return {}

    @classmethod
    def update_wallet_on_payment(cls, phone_number, paid_amount, liter):
        user = session.query(UserTable).filter_by(phone_number=phone_number).first()
        fkUserId = user.id
        current_wallet = session.query(WalletTable).filter_by(phone_number=phone_number).first()
        if current_wallet is not None:
            current_tl = current_wallet.tl
            current_mock_token = current_wallet.mock_token

            mock_token = current_mock_token + liter
            tl = current_tl - float(paid_amount)
            mock_token_to_tl = mock_token / 0.5
            total = tl + mock_token_to_tl

            new_wallet = session.query(WalletTable).filter(fkUserId == fkUserId).one()
            new_wallet.tl = tl
            new_wallet.mock_token = mock_token
            new_wallet.mock_token_to_tl = mock_token_to_tl
            new_wallet.tl_to_mock_token = current_wallet.tl_to_mock_token
            new_wallet.total = total
            session.commit()

            return {"tl": tl,
                    "mock_token": mock_token,
                    "mock_token_to_tl": mock_token_to_tl,
                    "total": total}
        return {}
