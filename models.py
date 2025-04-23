from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    resources = db.relationship('Resource', backref='owner', lazy='dynamic')
    requests = db.relationship('Request', backref='requester', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    available_from = db.Column(db.DateTime, nullable=False)
    available_to = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # A resource can have many allocations
    allocations = db.relationship('Allocation', backref='resource', lazy='dynamic')

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_type = db.Column(db.String(50))
    needed_from = db.Column(db.DateTime, nullable=False)
    needed_to = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, default=5)  # 1-10, higher is more important
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='pending')  # pending, allocated, denied
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # A request can have one allocation
    allocation = db.relationship('Allocation', backref='request', uselist=False)

class Allocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    allocated_from = db.Column(db.DateTime, nullable=False)
    allocated_to = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)