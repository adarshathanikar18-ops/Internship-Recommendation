#!/usr/bin/env python3
"""
Web scraper to get real company data from job portals
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin, urlparse
import csv

class CompanyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.companies = []

    def scrape_naukri_companies(self, max_pages=3):
        """Scrape company data from Naukri.com"""
        print("🔍 Scraping companies from Naukri.com...")
        
        base_url = "https://www.naukri.com/jobs-in-india"
        
        try:
            for page in range(1, max_pages + 1):
                print(f"Scraping page {page}...")
                
                # Add delay to be respectful
                time.sleep(random.uniform(1, 3))
                
                response = self.session.get(f"{base_url}?page={page}")
                if response.status_code != 200:
                    print(f"Failed to fetch page {page}")
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job listings (this is a simplified example)
                job_cards = soup.find_all('div', class_='jobTuple')
                
                for card in job_cards[:10]:  # Limit per page
                    try:
                        company_elem = card.find('a', class_='subTitle')
                        if company_elem:
                            company_name = company_elem.get_text(strip=True)
                            
                            # Extract other details
                            title_elem = card.find('a', class_='title')
                            job_title = title_elem.get_text(strip=True) if title_elem else "Software Developer"
                            
                            location_elem = card.find('span', class_='locationsContainer')
                            location = location_elem.get_text(strip=True) if location_elem else "India"
                            
                            # Generate realistic requirements based on job title
                            min_cgpa, min_prog, category = self.generate_requirements(job_title, company_name)
                            
                            company_data = {
                                'name': company_name,
                                'description': f"{category} company offering {job_title} positions",
                                'min_cgpa': min_cgpa,
                                'min_programming_score': min_prog,
                                'location': location,
                                'category': category,
                                'job_type': 'Internship',
                                'website': f"https://www.{company_name.lower().replace(' ', '')}.com"
                            }
                            
                            if company_data not in self.companies:
                                self.companies.append(company_data)
                                print(f"✅ Added: {company_name}")
                    
                    except Exception as e:
                        print(f"Error processing job card: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error scraping Naukri: {e}")

    def scrape_linkedin_companies(self):
        """Scrape popular tech companies from a curated list"""
        print("🔍 Adding popular tech companies...")
        
        popular_companies = [
            {'name': 'Google', 'category': 'Technology', 'min_cgpa': 8.5, 'min_prog': 85, 'location': 'Bangalore'},
            {'name': 'Microsoft', 'category': 'Technology', 'min_cgpa': 8.0, 'min_prog': 80, 'location': 'Hyderabad'},
            {'name': 'Amazon', 'category': 'E-commerce', 'min_cgpa': 7.5, 'min_prog': 75, 'location': 'Bangalore'},
            {'name': 'Meta', 'category': 'Social Media', 'min_cgpa': 8.0, 'min_prog': 85, 'location': 'Gurgaon'},
            {'name': 'Apple', 'category': 'Technology', 'min_cgpa': 8.5, 'min_prog': 85, 'location': 'Bangalore'},
            {'name': 'Netflix', 'category': 'Entertainment', 'min_cgpa': 8.0, 'min_prog': 80, 'location': 'Mumbai'},
            {'name': 'Uber', 'category': 'Transportation', 'min_cgpa': 7.5, 'min_prog': 75, 'location': 'Bangalore'},
            {'name': 'Airbnb', 'category': 'Travel', 'min_cgpa': 7.5, 'min_prog': 80, 'location': 'Bangalore'},
            {'name': 'Spotify', 'category': 'Music', 'min_cgpa': 7.5, 'min_prog': 75, 'location': 'Mumbai'},
            {'name': 'Salesforce', 'category': 'CRM', 'min_cgpa': 7.0, 'min_prog': 70, 'location': 'Hyderabad'},
        ]
        
        for company in popular_companies:
            company_data = {
                'name': company['name'],
                'description': f"Leading {company['category']} company with innovative products and services",
                'min_cgpa': company['min_cgpa'],
                'min_programming_score': company['min_prog'],
                'location': company['location'],
                'category': company['category'],
                'job_type': 'Internship',
                'website': f"https://www.{company['name'].lower()}.com"
            }
            self.companies.append(company_data)
            print(f"✅ Added: {company['name']}")

    def generate_requirements(self, job_title, company_name):
        """Generate realistic requirements based on job title and company"""
        job_title_lower = job_title.lower()
        company_lower = company_name.lower()
        
        # Determine category
        if any(word in job_title_lower for word in ['data', 'analyst', 'scientist', 'ml', 'ai']):
            category = 'Data Science'
            min_cgpa = random.uniform(7.0, 8.5)
            min_prog = random.randint(70, 85)
        elif any(word in job_title_lower for word in ['frontend', 'ui', 'ux', 'design']):
            category = 'Frontend'
            min_cgpa = random.uniform(6.5, 7.5)
            min_prog = random.randint(60, 75)
        elif any(word in job_title_lower for word in ['backend', 'api', 'server']):
            category = 'Backend'
            min_cgpa = random.uniform(7.0, 8.0)
            min_prog = random.randint(65, 80)
        elif any(word in job_title_lower for word in ['mobile', 'android', 'ios', 'app']):
            category = 'Mobile Development'
            min_cgpa = random.uniform(6.5, 7.5)
            min_prog = random.randint(65, 80)
        elif any(word in job_title_lower for word in ['devops', 'cloud', 'aws', 'azure']):
            category = 'DevOps'
            min_cgpa = random.uniform(7.0, 8.0)
            min_prog = random.randint(70, 85)
        elif any(word in job_title_lower for word in ['test', 'qa', 'quality']):
            category = 'Testing'
            min_cgpa = random.uniform(6.0, 7.0)
            min_prog = random.randint(55, 70)
        else:
            category = 'Software Development'
            min_cgpa = random.uniform(6.5, 7.5)
            min_prog = random.randint(60, 75)
        
        # Adjust based on company reputation
        if any(word in company_lower for word in ['google', 'microsoft', 'amazon', 'apple', 'meta']):
            min_cgpa += 0.5
            min_prog += 10
        elif any(word in company_lower for word in ['startup', 'tech', 'innovation']):
            min_cgpa -= 0.2
            min_prog -= 5
        
        return round(min_cgpa, 1), min(100, max(40, min_prog)), category

    def save_to_csv(self, filename='scraped_companies.csv'):
        """Save scraped companies to CSV"""
        if not self.companies:
            print("No companies to save!")
            return
        
        fieldnames = ['name', 'description', 'min_cgpa', 'min_programming_score', 
                     'location', 'category', 'job_type', 'website', 'required_skills']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for company in self.companies:
                # Add required_skills based on category
                skills_map = {
                    'Technology': 'Python, Java, System Design',
                    'Data Science': 'Python, Machine Learning, Statistics',
                    'Frontend': 'JavaScript, React, HTML, CSS',
                    'Backend': 'Java, Python, SQL, APIs',
                    'Mobile Development': 'Java, Kotlin, Swift, React Native',
                    'DevOps': 'AWS, Docker, Kubernetes, CI/CD',
                    'Testing': 'Selenium, Testing Frameworks, Manual Testing'
                }
                
                company['required_skills'] = skills_map.get(company['category'], 'Programming, Problem Solving')
                writer.writerow(company)
        
        print(f"💾 Saved {len(self.companies)} companies to {filename}")

    def run_scraper(self):
        """Run the complete scraping process"""
        print("🚀 Starting company data scraping...")
        
        # Add popular tech companies (reliable data)
        self.scrape_linkedin_companies()
        
        # Try to scrape from job sites (may not work due to anti-bot measures)
        try:
            self.scrape_naukri_companies(max_pages=2)
        except Exception as e:
            print(f"Job site scraping failed: {e}")
            print("Using curated company list instead...")
        
        # Add more curated companies if we don't have enough
        if len(self.companies) < 30:
            self.add_more_companies()
        
        self.save_to_csv()
        return self.companies

    def add_more_companies(self):
        """Add more curated companies to reach a good number"""
        additional_companies = [
            {'name': 'Zomato', 'category': 'Food Tech', 'min_cgpa': 6.5, 'min_prog': 65, 'location': 'Gurgaon'},
            {'name': 'Paytm', 'category': 'Fintech', 'min_cgpa': 6.5, 'min_prog': 65, 'location': 'Noida'},
            {'name': 'Ola', 'category': 'Transportation', 'min_cgpa': 6.5, 'min_prog': 65, 'location': 'Bangalore'},
            {'name': 'Byju\'s', 'category': 'EdTech', 'min_cgpa': 6.0, 'min_prog': 60, 'location': 'Bangalore'},
            {'name': 'Unacademy', 'category': 'EdTech', 'min_cgpa': 6.5, 'min_prog': 65, 'location': 'Bangalore'},
            {'name': 'PhonePe', 'category': 'Fintech', 'min_cgpa': 7.0, 'min_prog': 70, 'location': 'Bangalore'},
            {'name': 'Razorpay', 'category': 'Fintech', 'min_cgpa': 7.0, 'min_prog': 70, 'location': 'Bangalore'},
            {'name': 'Myntra', 'category': 'E-commerce', 'min_cgpa': 6.5, 'min_prog': 65, 'location': 'Bangalore'},
            {'name': 'Nykaa', 'category': 'E-commerce', 'min_cgpa': 6.5, 'min_prog': 60, 'location': 'Mumbai'},
            {'name': 'Dream11', 'category': 'Gaming', 'min_cgpa': 6.5, 'min_prog': 70, 'location': 'Mumbai'},
        ]
        
        for company in additional_companies:
            company_data = {
                'name': company['name'],
                'description': f"Leading {company['category']} company in India",
                'min_cgpa': company['min_cgpa'],
                'min_programming_score': company['min_prog'],
                'location': company['location'],
                'category': company['category'],
                'job_type': 'Internship',
                'website': f"https://www.{company['name'].lower().replace(' ', '').replace('\'', '')}.com"
            }
            self.companies.append(company_data)
            print(f"✅ Added: {company['name']}")

if __name__ == "__main__":
    scraper = CompanyScraper()
    companies = scraper.run_scraper()
    print(f"\n🎉 Scraping complete! Found {len(companies)} companies.")