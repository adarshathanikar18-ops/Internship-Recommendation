# Internship Recommendation System

A Flask-based web application that recommends companies and internships to students based on their academic performance, programming skills, and profile information.

## Features

- **Student Profile Input**: Collect CGPA, programming scores, skills, and achievements
- **Student & Company Registration**: Dedicated onboarding flows for students and partner companies
- **Smart Recommendations**: Uses machine learning (K-Nearest Neighbors) to match students with suitable companies
- **Subject-wise Matching**: Capture DSA, DBMS, OS, and ML marks to increase match accuracy
- **Transparent Explanations**: Each recommendation shows exactly how the match score was computed
- **Real Company Data**: Web-scraped data from 20+ companies including Google, Microsoft, Amazon, and more
- **Match Scoring**: Provides percentage match scores for each recommendation
- **Apply to Real Jobs**: Direct redirects to actual job listings on Naukri.com, LinkedIn, and company career pages
- **Application Tracking**: Track your applications across multiple platforms
- **Multiple Apply Channels**: Choose from Naukri, LinkedIn, or company careers page
- **Responsive UI**: Clean, modern interface built with Tailwind CSS

## 🚀 Quick Start

### **One-Click Setup (Recommended)**

#### **Windows:**
```cmd
# Double-click setup.bat or run:
setup.bat
```

#### **macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### **Manual Setup**
See detailed instructions in [`SETUP_GUIDE.md`](SETUP_GUIDE.md)

### **What You Get:**
- ✅ AI-powered internship recommendations
- ✅ 20+ real companies (Google, Microsoft, Amazon, etc.)
- ✅ Direct links to job portals (Naukri, LinkedIn, Company careers)
- ✅ Application tracking system
- ✅ Modern responsive UI

### **Access Application:**
After setup, visit: `http://127.0.0.1:5000`

## How It Works

1. **Data Collection**: Students enter their profile information including CGPA, programming score (0-100), skills, and achievements
2. **Feature Matching**: The system uses a K-Nearest Neighbors algorithm to find companies with similar requirements
3. **Scoring**: Each recommendation gets a match score based on how well the student's profile aligns with company requirements
4. **Results**: Top 5 recommended companies are displayed with match scores and descriptions
5. **Apply Process**: Students can apply through multiple channels:
   - **Naukri.com**: India's leading job portal
   - **LinkedIn**: Professional networking platform
   - **Company Careers**: Official company career pages
6. **Real Applications**: Students are redirected to actual job listings on external platforms

## Project Structure

```
├── app.py                    # Main Flask application
├── models.py                 # Database models (Student, Company, Application)
├── manage_companies.py       # Unified seeding & update utilities
├── model_training.py         # ML model training script
├── scraper.py                # Web scraper for company data
├── add_job_urls.py           # Script to add job portal URLs
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration
├── model.pkl                 # Trained ML model
├── setup.bat                 # Windows setup script
├── setup.sh                  # Linux/macOS setup script
├── SETUP_GUIDE.md           # Detailed setup instructions
├── QUICK_START.md           # Quick start guide
├── templates/                # HTML templates
│   ├── index.html           # Modern landing page
│   ├── form.html            # Enhanced student profile form
│   ├── result.html          # Recommendations with match scores
│   ├── company_details.html # Detailed company information
│   ├── applications.html    # Application tracking page
│   └── apply_redirect.html  # Job portal selection page
├── static/js/               # JavaScript files
│   └── script.js           # Form validation and interactions
└── instance/               # Database files
    └── company_reco.db     # SQLite database
```

## Configuration

The application uses SQLite by default. To use MySQL, update the `.env` file:

```env
DATABASE_URI=mysql+mysqlconnector://username:password@localhost:3306/database_name
```

## Company Data Management

Use the unified `manage_companies.py` script to seed or refresh company records:

```bash
# Seed database only if it's empty (defaults to sample_companies.csv)
python manage_companies.py seed --csv path/to/sample_companies.csv

# Refresh everything from a CSV export
python manage_companies.py update --source csv --csv scraped_companies.csv

# Refresh using the scraper (optionally limit results)
python manage_companies.py update --source scraper --limit 25
```

## Sample Companies

The system includes 20 pre-loaded companies:
- **Tech Giants**: Google, Microsoft, Amazon, Apple
- **IT Services**: TCS, Infosys, Wipro, Cognizant
- **Startups**: Flipkart, Zoho, AccioJob
- **Consulting**: Accenture, Deloitte, Capgemini

## Testing

Run the test script to verify everything works:
```bash
python test_app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Future Enhancements

- Add more sophisticated ML algorithms
- Include location-based filtering
- Add user authentication
- Implement company feedback system
- Add skill-based matching weights

## License

This project is open source and available under the MIT License.
