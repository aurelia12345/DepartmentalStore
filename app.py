import os

from flask import Flask
from api import ns, loc, dept, category, sub_category, user_ns
from extensions import api, db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)
    api.add_namespace(loc)
    api.add_namespace(dept)
    api.add_namespace(category)
    api.add_namespace(sub_category)
    api.add_namespace(user_ns)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()

