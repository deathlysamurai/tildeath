from . import db
from flask_login import UserMixin
from sqlalchemy.orm import class_mapper, ColumnProperty

ACCESS = {
    'user': 0,
    'admin': 1
}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    passphrase = db.Column(db.String(150), nullable=False)
    access = db.Column(db.Integer, default=0, nullable=False)

    def is_admin(self):
        return self.access == ACCESS['admin']
    
    def allowed(self, access_level):
        return self.access >= access_level
    
    def table_columns(self):
        hidden_props = ["id"]
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty) and not prop.key in hidden_props]