from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    registrations = db.relationship('Registration', back_populates='student', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'student_id': self.student_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    instructor = db.Column(db.String(100))
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer, default=30)
    enrolled = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    registrations = db.relationship('Registration', back_populates='course', lazy='dynamic')
    
    def is_full(self):
        return self.enrolled >= self.capacity
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'credits': self.credits,
            'instructor': self.instructor,
            'description': self.description,
            'capacity': self.capacity,
            'enrolled': self.enrolled,
            'is_full': self.is_full()
        }

class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(2))
    
    student = db.relationship('Student', back_populates='registrations')
    course = db.relationship('Course', back_populates='registrations')
    
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_registration'),)
