import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import joblib

# Load companies from database for more realistic data
from flask import Flask
from models import db, Company
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

companies = []
with app.app_context():
    db_companies = Company.query.all()
    for i, comp in enumerate(db_companies, 1):
        companies.append({
            'id': i,
            'name': comp.name,
            'min_cgpa': comp.min_cgpa,
            'min_prog': comp.min_programming_score,
            'category': comp.location or 'Technology'  # Use location as category for now
        })

# Create feature matrix for training
X = np.array([[c['min_cgpa'], c['min_prog']] for c in companies])

# Train KNN model
nbrs = NearestNeighbors(n_neighbors=8, metric='euclidean')
nbrs.fit(X)

model_pkg = {'model': nbrs, 'companies': companies}
joblib.dump(model_pkg, 'model.pkl')
print(f'Saved model.pkl with {len(companies)} companies')
