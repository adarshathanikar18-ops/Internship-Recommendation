#!/usr/bin/env python3
"""
Unified utility script for seeding and refreshing company data.

Usage examples:
    python manage_companies.py seed --csv sample_companies.csv
    python manage_companies.py update --csv scraped_companies.csv
    python manage_companies.py update --source scraper
"""
import argparse
import csv
import os
from typing import Iterable, Optional

from dotenv import load_dotenv
from flask import Flask

from models import Company, db
from scraper import CompanyScraper

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def parse_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def load_companies_from_csv(csv_path: str) -> Iterable[dict]:
    with open(csv_path, newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield {
                'name': row.get('name'),
                'description': row.get('description'),
                'min_cgpa': parse_float(row.get('min_cgpa')),
                'required_skills': row.get('required_skills'),
                'min_programming_score': parse_int(row.get('min_programming_score')),
                'min_dsa_score': parse_int(row.get('min_dsa_score')),
                'min_database_score': parse_int(row.get('min_database_score')),
                'min_os_score': parse_int(row.get('min_os_score')),
                'min_ml_score': parse_int(row.get('min_ml_score')),
                'website': row.get('website'),
                'location': row.get('location'),
                'job_type': row.get('job_type', 'Internship'),
                'naukri_url': row.get('naukri_url'),
                'linkedin_url': row.get('linkedin_url'),
                'company_careers_url': row.get('company_careers_url'),
            }


def create_company(row: dict) -> Company:
    return Company(
        name=row['name'],
        description=row.get('description'),
        min_cgpa=row.get('min_cgpa', 0.0),
        required_skills=row.get('required_skills'),
        min_programming_score=row.get('min_programming_score', 0),
        min_dsa_score=row.get('min_dsa_score', 0),
        min_database_score=row.get('min_database_score', 0),
        min_os_score=row.get('min_os_score', 0),
        min_ml_score=row.get('min_ml_score', 0),
        website=row.get('website'),
        location=row.get('location'),
        job_type=row.get('job_type') or 'Internship',
        naukri_url=row.get('naukri_url'),
        linkedin_url=row.get('linkedin_url'),
        company_careers_url=row.get('company_careers_url'),
    )


def seed_from_csv(csv_path: str):
    if not os.path.exists(csv_path):
        print(f"❌ CSV file '{csv_path}' not found.")
        return

    with app.app_context():
        db.create_all()
        if Company.query.count() > 0:
            print("ℹ️  Companies already exist. Skipping seed.")
            return

        print(f"🌱 Seeding companies from '{csv_path}'...")
        for row in load_companies_from_csv(csv_path):
            db.session.add(create_company(row))
        db.session.commit()
        print(f"✅ Seeded {Company.query.count()} companies.")


def refresh_from_csv(csv_path: str):
    if not os.path.exists(csv_path):
        print(f"❌ CSV file '{csv_path}' not found.")
        return

    with app.app_context():
        print(f"♻️  Refreshing database from '{csv_path}'...")
        Company.query.delete()
        for row in load_companies_from_csv(csv_path):
            db.session.add(create_company(row))
        db.session.commit()
        print(f"✅ Loaded {Company.query.count()} companies from CSV.")


def refresh_from_scraper(limit: Optional[int] = None):
    scraper = CompanyScraper()
    print("🕸️  Running scraper...")
    companies = scraper.run_scraper()
    if limit:
        companies = companies[:limit]

    with app.app_context():
        print("♻️  Refreshing database with scraped data...")
        Company.query.delete()
        for data in companies:
            db.session.add(create_company({
                'name': data.get('name'),
                'description': data.get('description'),
                'min_cgpa': data.get('min_cgpa'),
                'required_skills': data.get('required_skills'),
                'min_programming_score': data.get('min_programming_score'),
                'website': data.get('website'),
                'location': data.get('location'),
                'job_type': data.get('job_type'),
            }))
        db.session.commit()
        print(f"✅ Loaded {Company.query.count()} scraped companies.")


def main():
    parser = argparse.ArgumentParser(description="Manage company data.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    seed_parser = subparsers.add_parser('seed', help='Seed database if empty using CSV')
    seed_parser.add_argument('--csv', default='sample_companies.csv', help='Path to CSV file')

    update_parser = subparsers.add_parser('update', help='Refresh database from a source')
    update_parser.add_argument('--source', choices=['csv', 'scraper'], default='csv')
    update_parser.add_argument('--csv', default='scraped_companies.csv', help='CSV path when using csv source')
    update_parser.add_argument('--limit', type=int, help='Optional limit when scraping')

    args = parser.parse_args()

    if args.command == 'seed':
        seed_from_csv(args.csv)
    elif args.command == 'update':
        if args.source == 'csv':
            refresh_from_csv(args.csv)
        else:
            refresh_from_scraper(args.limit)


if __name__ == '__main__':
    main()

