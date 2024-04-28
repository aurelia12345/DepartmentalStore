import datetime
import jwt
import os

from flask import jsonify, request, abort, make_response
from flask_restx import Resource, Namespace
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from resource_models import Location, Department, Category, User
from api_models import (location_model, department_model, category_model,
                        sub_category_model, create_department_model, create_category_model,
                        create_sub_category_model, user_model, admin_model)
from models_dao import LocationDAO, DepartmentDAO, CategoryDAO, SubCategoryDAO, UserDAO

loc = Namespace("api/v1/location", description='API version v1 for location')
dept = Namespace("api/v1/department", description='API version v1 for department')
category = Namespace("api/v1/category", description='API version v1 for category')
sub_category = Namespace("api/v1/sub_category", description='API version v1 for sub_category')
user_ns = Namespace("api/v1/user", description='API version v1 for user signup, login')
ns = Namespace("api/v1", description='API version v1')

location_dao = LocationDAO()
department_dao = DepartmentDAO()
category_dao = CategoryDAO()
sub_category_dao = SubCategoryDAO()
user_dao = UserDAO()


@user_ns.route('/signup')
class Signup(Resource):
    @user_ns.expect(admin_model)
    def post(self):
        data = user_ns.payload
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        data['password'] = hashed_password
        user_dao.create(data)
        return make_response(jsonify({'message': 'User created successfully'}), 201)


@user_ns.route('/login', methods=['POST'])
class Login(Resource):
    @user_ns.expect(user_model)
    def post(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = User.query.filter_by(username=auth.username).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)},
                os.environ.get('SECRET_KEY'))
            return jsonify({'token': token})

        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, 'Token is missing')
        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
            user = User.query.get(data['id'])
            if not user:
                abort(401, 'Invalid token')
        except jwt.ExpiredSignatureError:
            abort(401, 'Token is expired')
        except jwt.InvalidTokenError:
            abort(401, 'Invalid token')
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            abort(401, 'Token is missing')

        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
            user = User.query.get(data['id'])
            if not user.admin:
                abort(403, 'Admin access required')
        except jwt.ExpiredSignatureError:
            abort(401, 'Token is expired')
        except jwt.InvalidTokenError:
            abort(401, 'Invalid token')

        return func(*args, **kwargs)

    return wrapper


@loc.route('/')
class ListLocationAPI(Resource):
    @login_required
    @loc.marshal_with(location_model)
    def get(self):
        return location_dao.get(), 200

    @login_required
    @admin_required
    @loc.expect(location_model)
    def post(self):
        try:
            data = loc.payload
            msg = location_dao.create(data)
            return make_response(jsonify({'message': msg}), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


@loc.route('/<int:location_id>')
class LocationAPI(Resource):
    @login_required
    @loc.marshal_with(location_model)
    def get(self, location_id):
        return location_dao.get(location_id), 200

    @login_required
    @admin_required
    @loc.expect(location_model)
    def put(self, location_id):
        try:
            data = loc.payload
            msg = location_dao.update(location_id, data)
            return make_response(jsonify({'message': msg}), 201)

        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    @login_required
    @admin_required
    def delete(self, location_id):
        try:
            msg = location_dao.delete(location_id)
            return make_response(jsonify({'message': msg}), 200)

        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


@dept.route('/')
class ListDepartmentsAPI(Resource):
    @login_required
    @dept.marshal_list_with(department_model)
    def get(self):
        return department_dao.get(), 200

    @login_required
    @admin_required
    @dept.expect(create_department_model)
    def post(self):
        try:
            data = dept.payload
            msg = department_dao.create(data)
            return make_response(jsonify({'message': msg}), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


@dept.route('/<int:department_id>')
class DepartmentAPI(Resource):
    @login_required
    @dept.marshal_with(department_model)
    def get(self, department_id):
        return department_dao.get(department_id), 200

    @login_required
    @admin_required
    @dept.expect(create_department_model)
    def put(self, department_id):
        try:
            data = dept.payload
            msg = department_dao.update(department_id, data)
            return make_response(jsonify({'message': msg}), 201)

        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    @login_required
    @admin_required
    def delete(self, department_id):
        try:
            msg = department_dao.delete(department_id)
            return make_response(jsonify({'message': msg}), 200)

        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


@category.route('/')
class ListCategoryAPI(Resource):
    # @login_required
    @category.marshal_list_with(category_model)
    def get(self):
        return category_dao.get(), 200

    @login_required
    @admin_required
    @category.expect(create_category_model)
    def post(self):
        try:
            data = category.payload
            msg = category_dao.create(data)
            return make_response(jsonify({'message': msg}), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


@category.route('/<int:category_id>')
class CategoryAPI(Resource):
    @login_required
    @category.marshal_with(category_model)
    def get(self, category_id):
        return category_dao.get(category_id), 200

    @login_required
    @admin_required
    @category.expect(create_category_model)
    def put(self, category_id):
        try:
            data = category.payload
            msg = category_dao.update(category_id, data)
            return make_response(jsonify({'message': msg}), 201)

        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    @login_required
    @admin_required
    def delete(self, category_id):
        try:
            msg = category_dao.delete(category_id)
            return make_response(jsonify({'message': msg}), 200)

        except Exception as e:
            return jsonify({'message': str(e)}), 500


@sub_category.route('/')
class ListSubCategoryAPI(Resource):
    @login_required
    @sub_category.marshal_list_with(sub_category_model)
    def get(self):
        return sub_category_dao.get(), 200

    @login_required
    @admin_required
    @sub_category.expect(create_sub_category_model)
    def post(self):
        try:
            data = sub_category.payload
            msg = sub_category_dao.create(data)
            return make_response(jsonify({'message': msg}), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


@sub_category.route('/<int:sub_category_id>')
class SubCategoryAPI(Resource):
    @login_required
    @sub_category.marshal_with(sub_category_model)
    def get(self, sub_category_id):
        return sub_category_dao.get(sub_category_id), 200

    @login_required
    @admin_required
    @sub_category.expect(create_sub_category_model)
    def put(self, sub_category_id):
        try:
            data = sub_category.payload
            msg = sub_category_dao.update(sub_category_id, data)
            return make_response(jsonify({'message': msg}), 201)

        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    @login_required
    @admin_required
    def delete(self, sub_category_id):
        try:
            msg = sub_category_dao.delete(sub_category_id)
            return make_response(jsonify({'message': msg}), 200)

        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


@ns.route('/locations/<int:location_id>/department')
class DepartmentAPI(Resource):
    @login_required
    @ns.marshal_list_with(department_model)
    def get(self, location_id):
        return Department.query.filter_by(location_id=location_id).all(), 200


@ns.route('/locations/<int:location_id>/department/<int:department_id>/category')
class CategoryAPI(Resource):
    @login_required
    @ns.marshal_list_with(category_model)
    def get(self, location_id, department_id):
        return Category.query.join(Department).join(Location).filter(
            Category.department_id == department_id,
            Department.location_id == location_id
        ).all(), 200
