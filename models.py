from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    cgpa = db.Column(db.Float, nullable=False)
    programming_score = db.Column(db.Integer, nullable=False)  # 0-100
    dsa_marks = db.Column(db.Integer, nullable=True)  # Data Structures & Algorithms
    database_marks = db.Column(db.Integer, nullable=True)  # DBMS
    os_marks = db.Column(db.Integer, nullable=True)  # Operating Systems
    ml_marks = db.Column(db.Integer, nullable=True)  # Machine Learning / AI
    skills = db.Column(db.String(500), nullable=True)  # comma-separated
    achievements = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    min_cgpa = db.Column(db.Float, default=0.0)
    required_skills = db.Column(db.String(500), nullable=True)  # comma-separated skills
    min_programming_score = db.Column(db.Integer, default=0)
    min_dsa_score = db.Column(db.Integer, default=0)
    min_database_score = db.Column(db.Integer, default=0)
    min_os_score = db.Column(db.Integer, default=0)
    min_ml_score = db.Column(db.Integer, default=0)
    website = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    job_type = db.Column(db.String(50), default='Internship')
    naukri_url = db.Column(db.String(300), nullable=True)
    linkedin_url = db.Column(db.String(300), nullable=True)
    company_careers_url = db.Column(db.String(300), nullable=True)

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    status = db.Column(db.String(50), default='Applied')  # Applied, Under Review, Accepted, Rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(500), nullable=True)
    
    # Relationships
    student = db.relationship('Student', backref='applications')
    company = db.relationship('Company', backref='applications')
