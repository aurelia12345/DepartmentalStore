from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

api = Api(version='1.0', title='DepartmentalStore API',
          description='DepartmentalStore Endpoints')
db = SQLAlchemy()

