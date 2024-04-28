from flask_restx import fields
from extensions import api

location_model = api.model("Location",{
    "name": fields.String(required=True, description='Name of the location'),
    "description": fields.String(description='Location Description'),
    # "department": fields.List(fields.Nested(department_model))
})

department_model = api.model("Department", {
    "name": fields.String(required=True, description='Name of the Department'),
    "location": fields.Nested(location_model)
})

create_department_model = api.model("Department", {
    "name": fields.String(required=True, description='Name of the Department'),
    "location_id": fields.Integer(required=True, description='The location id of the department')

})

category_model = api.model("Category", {
    "name": fields.String(required=True, description='Name of the category'),
    "department": fields.Nested(department_model)
})

create_category_model = api.model("Category", {
    "name": fields.String(required=True, description='Name of the Category'),
    "department_id": fields.Integer(required=True, description='The department id of the category')

})

sub_category_model = api.model("Sub-Category", {
    "name": fields.String(required=True, description='Name of the sub_category'),
    "category": fields.Nested(category_model)
})

create_sub_category_model = api.model("SubCategory", {
    "name": fields.String(required=True, description='Name of the SubCategory'),
    "category_id": fields.Integer(required=True, description='The category id of the SubCategory')

})

user_model = api.model("User", {
    "username": fields.String(required=True, description="Username of the user"),
    "password": fields.String(required=True, description="Password of the user"),
})

admin_model = api.inherit("AdminUser", user_model, {
    "admin": fields.Boolean(description="Admin access status", default=False)
})






