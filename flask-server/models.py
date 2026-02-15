from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.user_id)

class Flavor(db.Model):
   __tablename__ = 'flavors'
   flavorid = db.Column(db.Integer, primary_key=True)
   flavorname = db.Column(db.String(100))
   date_added = db.Column(db.Date)
   quantity = db.relationship('Quantity', back_populates='flavor', cascade='all, delete-orphan')

class Ingredient(db.Model):
   __tablename__ = 'ingredients'
   ingredientid = db.Column(db.Integer, primary_key=True)
   ingredientname = db.Column(db.String(400))
   availablequantity = db.Column(db.Float)
   date_added = db.Column(db.Date)
   quantity = db.relationship('Quantity', back_populates='ingredient', cascade='all, delete-orphan')


class Quantity(db.Model):
    __tablename__ = 'quantity'
    id = db.Column(db.Integer, primary_key=True)
    flavorid = db.Column(db.Integer, db.ForeignKey('flavors.flavorid'))
    ingredientid = db.Column(db.Integer, db.ForeignKey('ingredients.ingredientid'))
    date_added = db.Column(db.Date)
    date_updated = db.Column(db.Date)
    baseamount = db.Column(db.Float)
    unit =db.Column(db.String(10))

    # Relationships (many-to-one)
    flavor = db.relationship('Flavor', back_populates='quantity')
    ingredient = db.relationship('Ingredient', back_populates='quantity')

class batches(db.Model):
    __tablename__ = 'batches'
    batchid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    batchnumber = db.Column(db.String(100), unique=True)
    flavorid = db.Column(db.Integer, db.ForeignKey('flavors.flavorid'))
    bottles = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    flavor = db.relationship('Flavor', backref='batches')

class Containers(db.Model):
   __tablename__ = 'containers'
   containerid = db.Column(db.Integer, primary_key=True)
   containername = db.Column(db.String(100))
   availablecount = db.Column(db.Integer)
   date_updated = db.Column(db.Date)
