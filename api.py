from flask import jsonify
from flask_restx import Resource, Namespace
from resource_models import Location, Department, Category
from api_models import (location_model, department_model, category_model,
                        sub_category_model, create_department_model, create_category_model,
                        create_sub_category_model)
from models_dao import LocationDAO, DepartmentDAO, CategoryDAO, SubCategoryDAO

loc = Namespace("api/v1/location", description='API version v1 for location')
dept = Namespace("api/v1/department", description='API version v1 for department')
category = Namespace("api/v1/category", description='API version v1 for category')
sub_category = Namespace("api/v1/sub_category", description='API version v1 for sub_category')
ns = Namespace("api/v1", description='API version v1')


from functools import wraps
from flask import abort

from flask import request, redirect, url_for

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not user.is_authenticated:
            # Redirect to the login page if the user is not logged in
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            # Return a 403 Forbidden error if the user is not authenticated or not an admin
            abort(403)
        return func(*args, **kwargs)
    return decorated_function







location_dao = LocationDAO()
department_dao = DepartmentDAO()
category_dao = CategoryDAO()
sub_category_dao = SubCategoryDAO()


@loc.route('/')
class ListLocationAPI(Resource):
    @loc.marshal_with(location_model)
    def get(self):
        return location_dao.get(), 200

    @loc.expect(location_model)
    def post(self):
        try:
            data = loc.payload
            msg = location_dao.create(data)
            return jsonify({'message': msg}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 500


@loc.route('/<int:location_id>')
class LocationAPI(Resource):
    @loc.marshal_with(location_model)
    def get(self, location_id):
        return location_dao.get(location_id), 200

    @loc.expect(location_model)
    def put(self, location_id):
        try:
            data = loc.payload
            msg = location_dao.update(location_id, data)
            return jsonify({'message': msg}), 201

        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def delete(self, location_id):
        try:
            msg = location_dao.delete(location_id)
            return jsonify({'message': msg})

        except Exception as e:
            return jsonify({'message': str(e)}), 500


@dept.route('/')
class ListDepartmentsAPI(Resource):
    @dept.marshal_list_with(department_model)
    def get(self):
        return department_dao.get(), 200

    @dept.expect(create_department_model)
    def post(self):
        try:
            data = dept.payload
            msg = department_dao.create(data)
            return jsonify({'message': msg}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 500


@dept.route('/<int:department_id>')
class DepartmentAPI(Resource):
    @dept.marshal_with(department_model)
    def get(self, department_id):
        return department_dao.get(department_id), 200

    @dept.expect(create_department_model)
    def put(self, department_id):
        try:
            data = dept.payload
            msg = department_dao.update(department_id, data)
            return jsonify({'message': msg}), 201

        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def delete(self, department_id):
        try:
            msg = department_dao.delete(department_id)
            return jsonify({'message': msg})

        except Exception as e:
            return jsonify({'message': str(e)}), 500

@category.route('/')
class ListCategoryAPI(Resource):
    @category.marshal_list_with(category_model)
    def get(self):
        return category_dao.get(), 200

    @category.expect(create_category_model)
    def post(self):
        try:
            data = category.payload
            msg = category_dao.create(data)
            return jsonify({'message': msg}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 500


@category.route('/<int:category_id>')
class CategoryAPI(Resource):
    @category.marshal_with(category_model)
    def get(self, category_id):
        return category_dao.get(category_id), 200

    @category.expect(create_category_model)
    def put(self, category_id):
        try:
            data = category.payload
            msg = category_dao.update(category_id, data)
            return jsonify({'message': msg}), 201

        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def delete(self, category_id):
        try:
            msg = category_dao.delete(category_id)
            return jsonify({'message': msg})

        except Exception as e:
            return jsonify({'message': str(e)}), 500


@sub_category.route('/')
class ListSubCategoryAPI(Resource):
    @sub_category.marshal_list_with(sub_category_model)
    def get(self):
        return sub_category_dao.get(), 200

    @sub_category.expect(create_sub_category_model)
    def post(self):
        try:
            data = sub_category.payload
            msg = sub_category_dao.create(data)
            return jsonify({'message': msg}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 500


@sub_category.route('/<int:sub_category_id>')
class SubCategoryAPI(Resource):
    @category.marshal_with(sub_category_model)
    def get(self, sub_category_id):
        return sub_category_dao.get(sub_category_id), 200

    @category.expect(create_sub_category_model)
    def put(self, sub_category_id):
        try:
            data = sub_category.payload
            msg = sub_category_dao.update(sub_category_id, data)
            return jsonify({'message': msg}), 201

        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def delete(self, sub_category_id):
        try:
            msg = sub_category_dao.delete(sub_category_id)
            return jsonify({'message': msg})

        except Exception as e:
            return jsonify({'message': str(e)}), 500


@ns.route('/locations/<int:location_id>/department')
class DepartmentAPI(Resource):
    @ns.marshal_list_with(department_model)
    def get(self, location_id):
        return Department.query.filter_by(location_id=location_id).all()


@ns.route('/locations/<int:location_id>/department/<int:department_id>/category')
class CategoryAPI(Resource):
    @ns.marshal_list_with(category_model)
    def get(self, location_id, department_id):
        return Category.query.join(Department).join(Location).filter(
            Category.department_id == department_id,
            Department.location_id == location_id
        ).all()

