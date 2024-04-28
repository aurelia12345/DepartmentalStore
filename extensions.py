from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

api = Api(version='1.0', title='DepartmentalStore API',
          description='DepartmentalStore Endpoints',
          security='Bearer Auth')

# Define a security scheme
api.authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
db = SQLAlchemy()

