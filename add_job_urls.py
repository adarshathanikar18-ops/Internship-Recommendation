#!/usr/bin/env python3
"""
Add real job listing URLs to companies
"""
import os
from dotenv import load_dotenv
from flask import Flask
from models import db, Company
import urllib.parse

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def generate_job_urls():
    """Generate realistic job URLs for companies"""
    
    # Real job listing URLs (these are examples - in production you'd scrape actual URLs)
    job_urls = {
        'Google': {
            'naukri_url': 'https://www.naukri.com/google-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=google%20internship',
            'company_careers_url': 'https://careers.google.com/jobs/results/?category=DATA_CENTER_OPERATIONS&category=DEVELOPER_RELATIONS&category=HARDWARE_ENGINEERING&category=INFORMATION_TECHNOLOGY&category=MANUFACTURING_SUPPLY_CHAIN&category=NETWORK_ENGINEERING&category=PRODUCT_MANAGEMENT&category=PROGRAM_MANAGEMENT&category=SOFTWARE_ENGINEERING&category=TECHNICAL_INFRASTRUCTURE_ENGINEERING&category=TECHNICAL_WRITING&category=USER_EXPERIENCE&employment_type=INTERN'
        },
        'Microsoft': {
            'naukri_url': 'https://www.naukri.com/microsoft-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=microsoft%20internship',
            'company_careers_url': 'https://careers.microsoft.com/students/us/en/search-results?keywords=internship'
        },
        'Amazon': {
            'naukri_url': 'https://www.naukri.com/amazon-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=amazon%20internship',
            'company_careers_url': 'https://www.amazon.jobs/en/search?base_query=internship&loc_query='
        },
        'Meta': {
            'naukri_url': 'https://www.naukri.com/meta-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=meta%20internship',
            'company_careers_url': 'https://www.metacareers.com/jobs/?q=internship'
        },
        'Apple': {
            'naukri_url': 'https://www.naukri.com/apple-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=apple%20internship',
            'company_careers_url': 'https://jobs.apple.com/en-us/search?search=internship'
        },
        'Netflix': {
            'naukri_url': 'https://www.naukri.com/netflix-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=netflix%20internship',
            'company_careers_url': 'https://jobs.netflix.com/search?q=internship'
        },
        'Uber': {
            'naukri_url': 'https://www.naukri.com/uber-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=uber%20internship',
            'company_careers_url': 'https://www.uber.com/careers/list/?department=Engineering&team=University'
        },
        'Airbnb': {
            'naukri_url': 'https://www.naukri.com/airbnb-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=airbnb%20internship',
            'company_careers_url': 'https://careers.airbnb.com/positions/?search=internship'
        },
        'Spotify': {
            'naukri_url': 'https://www.naukri.com/spotify-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=spotify%20internship',
            'company_careers_url': 'https://www.lifeatspotify.com/jobs?q=internship'
        },
        'Salesforce': {
            'naukri_url': 'https://www.naukri.com/salesforce-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=salesforce%20internship',
            'company_careers_url': 'https://salesforce.wd1.myworkdayjobs.com/External_Career_Site?q=internship'
        },
        'Zomato': {
            'naukri_url': 'https://www.naukri.com/zomato-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=zomato%20internship',
            'company_careers_url': 'https://www.zomato.com/careers'
        },
        'Paytm': {
            'naukri_url': 'https://www.naukri.com/paytm-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=paytm%20internship',
            'company_careers_url': 'https://jobs.paytm.com/'
        },
        'Ola': {
            'naukri_url': 'https://www.naukri.com/ola-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=ola%20internship',
            'company_careers_url': 'https://www.olacabs.com/careers'
        },
        'Byju\'s': {
            'naukri_url': 'https://www.naukri.com/byjus-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=byjus%20internship',
            'company_careers_url': 'https://byjus.com/careers/'
        },
        'Unacademy': {
            'naukri_url': 'https://www.naukri.com/unacademy-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=unacademy%20internship',
            'company_careers_url': 'https://unacademy.com/careers'
        },
        'PhonePe': {
            'naukri_url': 'https://www.naukri.com/phonepe-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=phonepe%20internship',
            'company_careers_url': 'https://www.phonepe.com/careers/'
        },
        'Razorpay': {
            'naukri_url': 'https://www.naukri.com/razorpay-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=razorpay%20internship',
            'company_careers_url': 'https://razorpay.com/jobs/'
        },
        'Myntra': {
            'naukri_url': 'https://www.naukri.com/myntra-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=myntra%20internship',
            'company_careers_url': 'https://boards.greenhouse.io/myntra'
        },
        'Nykaa': {
            'naukri_url': 'https://www.naukri.com/nykaa-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=nykaa%20internship',
            'company_careers_url': 'https://www.nykaa.com/careers'
        },
        'Dream11': {
            'naukri_url': 'https://www.naukri.com/dream11-jobs',
            'linkedin_url': 'https://www.linkedin.com/jobs/search/?keywords=dream11%20internship',
            'company_careers_url': 'https://www.dream11.com/careers'
        }
    }
    
    return job_urls

def update_company_urls():
    """Update companies with job listing URLs"""
    job_urls = generate_job_urls()
    
    with app.app_context():
        companies = Company.query.all()
        updated_count = 0
        
        for company in companies:
            if company.name in job_urls:
                urls = job_urls[company.name]
                company.naukri_url = urls.get('naukri_url')
                company.linkedin_url = urls.get('linkedin_url')
                company.company_careers_url = urls.get('company_careers_url')
                updated_count += 1
                print(f"✅ Updated URLs for {company.name}")
            else:
                # Generate generic URLs for companies not in our list
                company_name_encoded = urllib.parse.quote(company.name.lower())
                company.naukri_url = f"https://www.naukri.com/{company_name_encoded}-jobs"
                company.linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={company_name_encoded}%20internship"
                company.company_careers_url = f"https://www.{company.name.lower().replace(' ', '').replace('\'', '')}.com/careers"
                updated_count += 1
                print(f"🔗 Generated URLs for {company.name}")
        
        db.session.commit()
        print(f"\n✅ Updated {updated_count} companies with job listing URLs")

if __name__ == "__main__":
    print("🔗 Adding job listing URLs to companies...")
    update_company_urls()
    print("🎉 Job URLs added successfully!")