# 🚀 InternMatch - Complete Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Optional: Advanced Setup](#optional-advanced-setup)

---

## 🔧 Prerequisites

### **Required Software:**
1. **Python 3.7 or higher** (Recommended: Python 3.9+)
2. **Git** (for cloning the repository)
3. **Web Browser** (Chrome, Firefox, Safari, Edge)

### **Optional but Recommended:**
- **Code Editor** (VS Code, PyCharm, Sublime Text)
- **Command Line Interface** (Terminal, PowerShell, Command Prompt)

---

## 💻 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10, macOS 10.14, Ubuntu 18.04 | Latest versions |
| **RAM** | 4GB | 8GB+ |
| **Storage** | 500MB free space | 1GB+ |
| **Python** | 3.7+ | 3.9+ |
| **Internet** | Required for initial setup | Stable connection |

---

## 📥 Installation Steps

### **Step 1: Install Python**

#### **Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.9+ for Windows
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### **macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
# Verify installation
python3 --version
pip3 --version
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

### **Step 2: Install Git**

#### **Windows:**
1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Install with default settings
3. Verify: `git --version`

#### **macOS:**
```bash
# Using Homebrew
brew install git

# Or use Xcode Command Line Tools
xcode-select --install
```

#### **Linux:**
```bash
sudo apt install git
```

### **Step 3: Clone the Repository**

```bash
# Clone the project
git clone <repository-url>
cd internship-recommendation-system

# Or if you have the project as a ZIP file:
# 1. Extract the ZIP file
# 2. Open terminal/command prompt in the extracted folder
```

### **Step 4: Create Virtual Environment**

#### **Windows:**
```cmd
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# You should see (.venv) in your command prompt
```

#### **macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# You should see (.venv) in your terminal prompt
```

### **Step 5: Install Dependencies**

```bash
# Make sure virtual environment is activated (you should see (.venv))
pip install -r requirements.txt

# This will install:
# - Flask (web framework)
# - Flask-SQLAlchemy (database)
# - scikit-learn (machine learning)
# - pandas, numpy (data processing)
# - requests, beautifulsoup4 (web scraping)
# - python-dotenv (environment variables)
```

### **Step 6: Set Up Database**

```bash
# Create and populate database with company data
python db_create.py

# You should see: "Creating tables..." and "Seeded companies."
```

### **Step 7: Train ML Model**

```bash
# Train the recommendation model
python model_training.py

# You should see: "Saved model.pkl with X companies"
```

---

## ⚙️ Configuration

### **Environment Variables (.env file)**

The `.env` file should already exist with default settings:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///company_reco.db
```

**For production, update:**
- Change `SECRET_KEY` to a secure random string
- Set `FLASK_ENV=production`
- Optionally use MySQL/PostgreSQL instead of SQLite

### **Database Configuration**

**Default (SQLite - Recommended for beginners):**
```env
DATABASE_URI=sqlite:///company_reco.db
```

**MySQL (Advanced):**
```env
DATABASE_URI=mysql+mysqlconnector://username:password@localhost:3306/database_name
```

---

## 🚀 Running the Application

### **Start the Application:**

```bash
# Make sure virtual environment is activated
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# Run the application
python app.py
```

### **Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### **Access the Application:**
1. Open your web browser
2. Go to: `http://127.0.0.1:5000` or `http://localhost:5000`
3. You should see the InternMatch homepage!

---

## 🔍 Verification Checklist

### **✅ Quick Test:**
1. **Homepage loads** - Should see modern landing page with "InternMatch" branding
2. **Click "Get My Recommendations"** - Should open profile form
3. **Fill out form** with sample data:
   - Name: "Test User"
   - CGPA: 7.5
   - Programming Score: 75
   - Skills: "Python, Java, SQL"
4. **Submit form** - Should see recommendations with match scores
5. **Click "Apply Now"** - Should see job portal options
6. **Click any portal** - Should redirect to external job site

### **✅ File Structure Check:**
```
internship-recommendation-system/
├── app.py ✓
├── models.py ✓
├── db_create.py ✓
├── model_training.py ✓
├── model.pkl ✓ (created after training)
├── requirements.txt ✓
├── .env ✓
├── templates/ ✓
├── static/ ✓
├── instance/
│   └── company_reco.db ✓ (created after db setup)
└── .venv/ ✓ (virtual environment)
```

---

## 🛠️ Troubleshooting

### **Common Issues & Solutions:**

#### **1. "python: command not found"**
**Solution:**
- **Windows**: Reinstall Python with "Add to PATH" checked
- **macOS/Linux**: Use `python3` instead of `python`

#### **2. "pip: command not found"**
**Solution:**
```bash
# Windows
python -m ensurepip --upgrade

# macOS/Linux
python3 -m ensurepip --upgrade
```

#### **3. "Permission denied" errors**
**Solution:**
- Make sure virtual environment is activated
- On Linux/macOS, don't use `sudo` with pip inside venv

#### **4. "Module not found" errors**
**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

#### **5. Database errors**
**Solution:**
```bash
# Delete database and recreate
rm instance/company_reco.db  # Linux/macOS
del instance\company_reco.db  # Windows

# Recreate database
python db_create.py
python model_training.py
```

#### **6. Port 5000 already in use**
**Solution:**
- Close other applications using port 5000
- Or modify `app.py` to use different port:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use port 5001
```

#### **7. Web scraping fails**
**Solution:**
- This is normal - the scraper may be blocked by websites
- The app will work with the pre-loaded company data
- Internet connection required for external job links

---

## 🔧 Optional: Advanced Setup

### **1. Update Company Data (Optional)**

```bash
# Scrape fresh company data (may not work due to anti-bot measures)
python scraper.py

# Update database with new data
python update_companies.py --csv scraped_companies.csv

# Add job portal URLs
python add_job_urls.py

# Retrain model with new data
python model_training.py
```

### **2. Production Deployment**

#### **Using Gunicorn (Linux/macOS):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### **Using Waitress (Windows):**
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### **3. Database Migration to MySQL**

```bash
# Install MySQL connector
pip install mysql-connector-python

# Update .env file
DATABASE_URI=mysql+mysqlconnector://user:password@localhost:3306/internmatch

# Recreate database
python db_create.py
```

---

## 📞 Support

### **If you encounter issues:**

1. **Check Python version**: `python --version` (should be 3.7+)
2. **Check virtual environment**: Look for `(.venv)` in terminal
3. **Check file permissions**: Ensure you can read/write in project folder
4. **Check internet connection**: Required for initial setup and job links
5. **Check logs**: Look at terminal output for error messages

### **Common Commands Reference:**

```bash
# Activate virtual environment
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# Deactivate virtual environment
deactivate

# Install new package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# Reset database
python db_create.py

# Retrain model
python model_training.py

# Run application
python app.py
```

---

## 🎉 Success!

If you can see the InternMatch homepage and submit a profile to get recommendations, **congratulations!** 🎊

You now have a fully functional AI-powered internship recommendation system running on your machine!

### **Next Steps:**
- Explore the application features
- Try different student profiles
- Click on company details and apply buttons
- Customize the company data or UI as needed

**Happy job hunting!** 🚀✨