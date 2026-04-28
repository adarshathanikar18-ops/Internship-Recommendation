import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, Student, Company, Application
import joblib
import numpy as np

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///company_reco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

db.init_app(app)

MODEL_PATH = 'model.pkl'

def load_model():
    if os.path.exists(MODEL_PATH):
        pkg = joblib.load(MODEL_PATH)
        return pkg
    else:
        from sklearn.neighbors import NearestNeighbors
        companies = [
            {'id': 1, 'name': 'Acme Corp', 'min_cgpa': 7.0, 'min_prog':70},
            {'id': 2, 'name': 'ByteWorks', 'min_cgpa': 6.5, 'min_prog':60},
            {'id': 3, 'name': 'DataDive', 'min_cgpa': 7.5, 'min_prog':75},
            {'id': 4, 'name': 'MobileMakers', 'min_cgpa': 6.0, 'min_prog':55},
            {'id': 5, 'name': 'FinSys', 'min_cgpa': 7.2, 'min_prog':70},
            {'id': 6, 'name': 'Webify', 'min_cgpa': 6.0, 'min_prog':50},
            {'id': 7, 'name': 'AI Labs', 'min_cgpa': 8.0, 'min_prog':85},
            {'id': 8, 'name': 'CloudScale', 'min_cgpa': 7.0, 'min_prog':65},
        ]
        X = np.array([[c['min_cgpa'], c['min_prog']] for c in companies])
        nbrs = NearestNeighbors(n_neighbors=5, metric='euclidean')
        nbrs.fit(X)
        return {'model': nbrs, 'companies': companies}

MODEL_PKG = load_model()

SUBJECT_FIELDS = [
    ('dsa_marks', 'Data Structures & Algorithms'),
    ('database_marks', 'Database Management Systems'),
    ('os_marks', 'Operating Systems'),
    ('ml_marks', 'Machine Learning & AI'),
]

MATCH_METRICS = [
    {
        'label': 'CGPA',
        'student_key': 'cgpa',
        'company_key': 'min_cgpa',
        'max_value': 10,
        'weight': 0.25,
        'unit': '/10'
    },
    {
        'label': 'Programming',
        'student_key': 'programming_score',
        'company_key': 'min_programming_score',
        'max_value': 100,
        'weight': 0.25,
        'unit': '/100'
    },
    {
        'label': 'DSA',
        'student_key': 'dsa_marks',
        'company_key': 'min_dsa_score',
        'max_value': 100,
        'weight': 0.15,
        'unit': '/100'
    },
    {
        'label': 'DBMS',
        'student_key': 'database_marks',
        'company_key': 'min_database_score',
        'max_value': 100,
        'weight': 0.15,
        'unit': '/100'
    },
    {
        'label': 'Operating Systems',
        'student_key': 'os_marks',
        'company_key': 'min_os_score',
        'max_value': 100,
        'weight': 0.1,
        'unit': '/100'
    },
    {
        'label': 'Machine Learning',
        'student_key': 'ml_marks',
        'company_key': 'min_ml_score',
        'max_value': 100,
        'weight': 0.1,
        'unit': '/100'
    }
]


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def collect_subject_scores(form):
    scores = {}
    for field, _ in SUBJECT_FIELDS:
        scores[field] = safe_int(form.get(field), 0)
    return scores


def fetch_company_pool():
    companies = Company.query.all()
    if companies:
        return [{
            'id': c.id,
            'name': c.name,
            'description': c.description or f"{c.location or 'Technology'} company",
            'category': c.location or 'Technology',
            'min_cgpa': c.min_cgpa or 0,
            'min_programming_score': c.min_programming_score or 0,
            'min_dsa_score': c.min_dsa_score or 0,
            'min_database_score': c.min_database_score or 0,
            'min_os_score': c.min_os_score or 0,
            'min_ml_score': c.min_ml_score or 0,
            'db_record': c,
        } for c in companies]

    fallback = []
    for c in MODEL_PKG['companies']:
        fallback.append({
            'id': c['id'],
            'name': c['name'],
            'description': c.get('description', f"{c.get('category', 'Technology')} company"),
            'category': c.get('category', 'Technology'),
            'min_cgpa': c.get('min_cgpa', 0),
            'min_programming_score': c.get('min_prog', 0),
            'min_dsa_score': c.get('min_dsa_score', 0),
            'min_database_score': c.get('min_database_score', 0),
            'min_os_score': c.get('min_os_score', 0),
            'min_ml_score': c.get('min_ml_score', 0),
            'db_record': None,
        })
    return fallback


def calculate_metric_score(student_value, company_value, max_value):
    student_value = max(0, student_value or 0)
    company_value = max(0, company_value or 0)
    max_value = max(max_value, 1)

    if company_value == 0 and student_value == 0:
        return 55.0

    diff = student_value - company_value
    if diff >= 0:
        boost = min(30, (diff / max_value) * 30)
        return round(70 + boost, 1)

    penalty = min(40, (abs(diff) / max_value) * 40)
    return round(max(25, 70 - penalty), 1)


def score_company(student_profile, company_meta):
    breakdown = []
    total_weight = sum(metric['weight'] for metric in MATCH_METRICS)
    weighted_score = 0

    for metric in MATCH_METRICS:
        student_value = student_profile.get(metric['student_key'], 0) or 0
        company_value = company_meta.get(metric['company_key'], 0) or 0
        metric_score = calculate_metric_score(student_value, company_value, metric['max_value'])
        weighted_score += metric_score * metric['weight']
        breakdown.append({
            'label': metric['label'],
            'student_value': student_value,
            'company_value': company_value,
            'score': metric_score,
            'unit': metric['unit'],
            'status': 'meets' if student_value >= company_value else 'gap'
        })

    final_score = round(weighted_score / total_weight, 1) if total_weight else 0
    meets_requirements = all(
        (student_profile.get(metric['student_key'], 0) or 0) >= (company_meta.get(metric['company_key'], 0) or 0)
        for metric in MATCH_METRICS
        if company_meta.get(metric['company_key'])
    )
    return final_score, breakdown, meets_requirements


def build_match_summary(breakdown):
    strengths = [item['label'] for item in breakdown if item['status'] == 'meets' and item['company_value']]
    gaps = [item['label'] for item in breakdown if item['status'] == 'gap' and item['company_value']]

    summary_parts = []
    if strengths:
        summary_parts.append(f"Strong in {', '.join(strengths[:2])}")
    if gaps:
        summary_parts.append(f"Consider improving {', '.join(gaps[:2])}")

    return ' • '.join(summary_parts) if summary_parts else 'Balanced profile match'


def build_student_profile_dict(student, subject_scores):
    profile = {
        'name': student.name,
        'email': student.email,
        'cgpa': student.cgpa,
        'programming_score': student.programming_score,
        'skills': student.skills,
        'achievements': student.achievements
    }
    profile.update(subject_scores)
    return profile


@app.route('/')
def index():
    student_id = session.get('student_id')
    student = None
    if student_id:
        student = db.session.get(Student, student_id)
    return render_template('index.html', logged_in=student is not None, student=student)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if not all([name, email, password]):
        flash('All fields are required', 'error')
        return redirect(url_for('signup'))
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('signup'))
    
    if len(password) < 6:
        flash('Password must be at least 6 characters', 'error')
        return redirect(url_for('signup'))
    
    existing = Student.query.filter_by(email=email).first()
    if existing:
        flash('Email already registered. Please log in.', 'error')
        return redirect(url_for('login'))
    
    student = Student(name=name, email=email, cgpa=0, programming_score=0)
    student.set_password(password)
    db.session.add(student)
    db.session.commit()
    
    session['student_id'] = student.id
    flash('Account created! Please complete your profile.', 'success')
    return redirect(url_for('recommend'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    student = Student.query.filter_by(email=email).first()
    if not student or not student.check_password(password):
        flash('Invalid email or password', 'error')
        return redirect(url_for('login'))
    
    session['student_id'] = student.id
    flash(f'Welcome back, {student.name}!', 'success')
    return redirect(url_for('my_applications'))

@app.route('/logout')
def logout():
    session.pop('student_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/recommend', methods=['GET', 'POST'])
@app.route('/register/student', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        return render_template('form.html', subject_fields=SUBJECT_FIELDS)

    name = request.form.get('name')
    email = request.form.get('email')
    cgpa = safe_float(request.form.get('cgpa'), 0.0)
    programming_score = safe_int(request.form.get('programming_score'), 0)
    skills = request.form.get('skills') or ''
    achievements = request.form.get('achievements') or ''
    subject_scores = collect_subject_scores(request.form)

    # Check if logged in user or existing email
    student_id = session.get('student_id')
    student = Student.query.get(student_id) if student_id else None
    
    if not student and email:
        student = Student.query.filter_by(email=email).first()
    
    if student:
        # Update existing student
        student.name = name
        student.email = email or student.email
        student.cgpa = cgpa
        student.programming_score = programming_score
        student.skills = skills
        student.achievements = achievements
        for field, value in subject_scores.items():
            setattr(student, field, value)
    else:
        # Create new student
        student = Student(
            name=name,
            email=email,
            cgpa=cgpa,
            programming_score=programming_score,
            skills=skills,
            achievements=achievements,
            **subject_scores
        )
        db.session.add(student)
    
    db.session.commit()

    # Create student dict for template (to avoid session issues)
    student_data = build_student_profile_dict(student, subject_scores)

    # Get recommendations from company pool
    student_profile = {
        'cgpa': cgpa,
        'programming_score': programming_score,
        **subject_scores
    }
    companies_meta = fetch_company_pool()

    results = []
    for company in companies_meta:
        final_score, breakdown, meets_requirements = score_company(student_profile, company)
        subject_requirements = {
            field: company.get(field_key, 0)
            for field, field_key in [
                ('dsa_marks', 'min_dsa_score'),
                ('database_marks', 'min_database_score'),
                ('os_marks', 'min_os_score'),
                ('ml_marks', 'min_ml_score')
            ]
        }

        results.append({
            'id': company['id'],
            'name': company['name'],
            'min_cgpa': company['min_cgpa'],
            'min_prog': company['min_programming_score'],
            'match_score': final_score,
            'description': company['description'],
            'category': company['category'],
            'meets_requirements': meets_requirements,
            'breakdown': breakdown,
            'match_summary': build_match_summary(breakdown),
            'subject_requirements': subject_requirements
        })

    # Sort by match score (highest first)
    results.sort(key=lambda x: x['match_score'], reverse=True)

    # Store student_id in session for apply functionality
    session['student_id'] = student.id

    return render_template(
        'result.html',
        results=results,
        student=student_data,
        subject_fields=SUBJECT_FIELDS
    )


@app.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'GET':
        return render_template('company_register.html', subject_fields=SUBJECT_FIELDS)

    name = request.form.get('name')
    if not name:
        flash('Company name is required', 'error')
        return redirect(url_for('register_company'))

    company = Company(
        name=name,
        description=request.form.get('description'),
        min_cgpa=safe_float(request.form.get('min_cgpa'), 0.0),
        min_programming_score=safe_int(request.form.get('min_programming_score'), 0),
        min_dsa_score=safe_int(request.form.get('min_dsa_score'), 0),
        min_database_score=safe_int(request.form.get('min_database_score'), 0),
        min_os_score=safe_int(request.form.get('min_os_score'), 0),
        min_ml_score=safe_int(request.form.get('min_ml_score'), 0),
        required_skills=request.form.get('required_skills'),
        website=request.form.get('website'),
        location=request.form.get('location'),
        job_type=request.form.get('job_type') or 'Internship',
        naukri_url=request.form.get('naukri_url'),
        linkedin_url=request.form.get('linkedin_url'),
        company_careers_url=request.form.get('company_careers_url')
    )

    db.session.add(company)
    db.session.commit()
    flash('Company registered successfully!', 'success')
    return redirect(url_for('company_details', company_id=company.id))

@app.route('/apply/<int:company_id>')
def apply_to_company(company_id):
    student_id = session.get('student_id')
    if not student_id:
        flash('Please complete your profile first', 'error')
        return redirect(url_for('recommend'))
    
    company = Company.query.get_or_404(company_id)
    
    # Check if already applied
    existing_app = Application.query.filter_by(
        student_id=student_id, 
        company_id=company_id
    ).first()
    
    if existing_app:
        flash('You have already applied to this company!', 'info')
        return redirect(url_for('my_applications'))
    
    # Create new application record for tracking
    application = Application(
        student_id=student_id,
        company_id=company_id,
        status='Redirected to Job Portal'
    )
    db.session.add(application)
    db.session.commit()
    
    # Redirect to actual job listing
    return render_template('apply_redirect.html', company=company)

@app.route('/apply/<int:company_id>/<platform>')
def apply_redirect(company_id, platform):
    """Redirect to specific job platform"""
    company = Company.query.get_or_404(company_id)
    
    url_map = {
        'naukri': company.naukri_url,
        'linkedin': company.linkedin_url,
        'careers': company.company_careers_url
    }
    
    redirect_url = url_map.get(platform)
    if redirect_url:
        return redirect(redirect_url)
    else:
        flash('Job listing URL not available', 'error')
        return redirect(url_for('company_details', company_id=company_id))

@app.route('/applications')
def my_applications():
    student_id = session.get('student_id')
    if not student_id:
        flash('Please complete your profile first', 'error')
        return redirect(url_for('recommend'))
    
    applications = db.session.query(Application, Company).join(
        Company, Application.company_id == Company.id
    ).filter(Application.student_id == student_id).all()
    
    student = Student.query.get(student_id)
    return render_template('applications.html', applications=applications, student=student)

@app.route('/company/<int:company_id>')
def company_details(company_id):
    company = Company.query.get_or_404(company_id)
    student_id = session.get('student_id')
    
    # Check if already applied
    has_applied = False
    if student_id:
        has_applied = Application.query.filter_by(
            student_id=student_id, 
            company_id=company_id
        ).first() is not None
    
    return render_template(
        'company_details.html',
        company=company,
        has_applied=has_applied,
        subject_fields=SUBJECT_FIELDS
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 🔥 Create tables before app runs
    app.run(debug=True)
