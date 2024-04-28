from resource_models import Location, Department, Category, SubCategory, User
from extensions import db


class BaseDAO():
    def __init__(self, model):
        self.model = model

    def get(self, obj_id=None):
        try:
            if obj_id:
                return self.model.query.get(obj_id)
            else:
                return self.model.query.all()
        except Exception as e:
            raise e

    def create(self, data):
        try:
            obj = self.model(**data)
            db.session.add(obj)
            db.session.commit()
            return "Created"
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()

    def update(self, obj_id, data):
        try:
            obj = self.model.query.get(obj_id)
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                db.session.commit()
                return "Updated"
            else:
                self.create(data)
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()

    def delete(self, obj_id):
        try:
            obj = self.model.query.get(obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return "Deleted"
            else:
                return f"{self.model.__name__} object not found"
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()


class LocationDAO(BaseDAO):
    def __init__(self):
        super().__init__(Location)


class DepartmentDAO(BaseDAO):
    def __init__(self):
        super().__init__(Department)


class CategoryDAO(BaseDAO):
    def __init__(self):
        super().__init__(Category)


class SubCategoryDAO(BaseDAO):
    def __init__(self):
        super().__init__(SubCategory)


class UserDAO(BaseDAO):
    def __init__(self):
        super().__init__(User)
