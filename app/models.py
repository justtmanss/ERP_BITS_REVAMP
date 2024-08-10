from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    students = db.relationship('Student', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    academic_year = db.Column(db.Integer, nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), nullable=True)
    finance_details = db.relationship('Finance', backref='student', lazy=True)
    demographic_details = db.relationship('Demographic', backref='student', lazy=True)
    registrations = db.relationship('Registration', backref='student', lazy=True)


class Specialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Course', backref='specialization', lazy=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), nullable=False)
    registrations = db.relationship('Registration', backref='course', lazy=True)


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester = db.Column(db.String(10), nullable=False)


class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    tuition_fee = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)


class Demographic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    emergency_contact = db.Column(db.String(150), nullable=False)
