from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    disease = db.Column(db.String(50))
    prediction = db.Column(db.Integer)
    risk_probability = db.Column(db.Float)
    risk_level = db.Column(db.String(20))
    suggestion = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)