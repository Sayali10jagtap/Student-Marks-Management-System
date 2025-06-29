from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    
    subject1 = db.Column(db.Integer, nullable=False)
    subject2 = db.Column(db.Integer, nullable=False)
    subject3 = db.Column(db.Integer, nullable=False)
    subject4 = db.Column(db.Integer, nullable=False)
    subject5 = db.Column(db.Integer, nullable=False)
    
    total = db.Column(db.Integer, nullable=False)
    average = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(2), nullable=False)
