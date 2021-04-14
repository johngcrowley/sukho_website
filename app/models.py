from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """USER MODEL"""

    __tablename__ = 'flasklogin-user'
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key = False,
        unique = False,
        nullable = False
    )
    def set_password(self, password):
        """Create hashed p/w"""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )
    def check_password(self, password):
        """Check hashed p/w"""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class employee(db.Model):
    """Data model for employees' information"""

    __tablename__ = 'employee'
    id = db.Column(
        db.Integer,
        unique=True, 
        primary_key=True
        )
    name = db.Column(
        db.String(64),
        unique=True,
        nullable=False
        )
    email = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )
    position = db.Column(
        db.String(64),
        nullable=False
    )
    admin = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )
    def __repr__(self):
        return "<employee {}>".format(self.name)

class tips(db.Model):
    """Data Model for tips by Date for each Server"""
   
    __tablename__ = 'tips'
    id = db.Column(
        db.Integer,
        primary_key=True
        )
    employee = db.Column(
        db.String(64),
        nullable=False
    )
    employee_id = db.Column(
        db.Integer
        )
    location = db.Column(
        db.String(64),
        nullable=False
    )
    tips = db.Column(
        db.Integer,
        nullable=False,
        )
    created_at = db.Column(
        db.DateTime,
        nullable=False)
    
    time = db.Column(
        db.String(64),
        nullable=True
    )
    

    def __repr__(self):
        return "<employee {}>".format(self.employee_id)