#!/usr/bin/env python
import os.path
from flask import Flask
from flask_cors import CORS
from views import CalculateDistancesAPI, ResultAPI
from database import db


def register_views(app):
    app.add_url_rule('/api/calculateDistances', view_func=CalculateDistancesAPI.as_view('distances'))
    app.add_url_rule('/api/getResult', view_func=ResultAPI.as_view('result'))


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['DATABASE_PATH'] = "data.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.config['DATABASE_PATH']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False
    db.init_app(app)
    register_views(app)
    return app


def setup_database(app):
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app = create_app()
    if not os.path.isfile(app.config['DATABASE_PATH']):
        setup_database(app)
    app.run(host='0.0.0.0')
