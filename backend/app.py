import datetime
from flask import Flask
from dotenv import load_dotenv
from os import path
import os

from flask_jwt_extended import JWTManager

env_var = os.getenv('FLASK_ENV')
if env_var == "production":
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, 'production.env'))
else:
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, 'development.env'))

from api.views import *


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user.bp)
    app.register_blueprint(plate.bp)
    app.register_blueprint(payment.bp)
    app.register_blueprint(wallet.bp)

    app.secret_key = os.getenv('SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)
    app.config['JWT_SECRET_KEY'] = "mock_pay_super_Secret_key"

    jwt = JWTManager(app)

    return app


app = create_app()
