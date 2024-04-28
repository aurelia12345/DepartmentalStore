import jwt
import datetime

from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace
from werkzeug.security import generate_password_hash, check_password_hash
from api import ns,loc, dept, category,sub_category
from extensions import api, db
from resource_models import User

user = Namespace("api/v1", description='API version v1 for user signup, login')


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config['SECRET_KEY'] = "my-secret-key-06041995"
    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)
    api.add_namespace(loc)
    api.add_namespace(dept)
    api.add_namespace(category)
    api.add_namespace(sub_category)

    return app

@user.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201


@user.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


if __name__ == "__main__":
    app = create_app()
    app.run()

