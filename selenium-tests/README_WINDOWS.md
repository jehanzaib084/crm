# Simple Frontend Tests for Windows

## 🚀 Quick Start

### Step 1: Install Python
- Download from: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation

### Step 2: Install Dependencies
Open Command Prompt (cmd) and run:
```bash
pip install selenium webdriver-manager
```

Or use the requirements file:
```bash
pip install -r requirements_simple.txt
```

### Step 3: Run Tests
```bash
python frontend_tests.py
```

**That's it!** 🎉

## 📋 What Gets Tested

1. **Test 1: Homepage Loads**
   - Opens your frontend URL
   - Verifies page loads
   - Takes screenshot

2. **Test 2: Login Functionality**
   - Finds login form
   - Fills in credentials
   - Clicks login button
   - Verifies form behavior

3. **Test 3: Frontend API Response**
   - Logs in via frontend
   - Checks if dashboard loads data
   - Verifies frontend-backend communication

4. **Test 4: Navigation & Buttons**
   - Tests navigation to Invoice page
   - Verifies buttons and links work
   - Checks interactive elements

## 📸 Screenshots

All screenshots are saved in `screenshots/` folder:
- `01_homepage.png`
- `02_login_page.png`
- `02_login_filled.png`
- `02_after_login.png`
- `03_dashboard.png`
- `04_invoice_page.png`

## ⚙️ Configuration

The test uses this URL (already configured):
```python
FRONTEND_URL = "http://20.239.224.248/"
```

To change it, edit `frontend_tests.py`:
```python
FRONTEND_URL = "http://your-url-here/"
EMAIL = "admin@admin.com"
PASSWORD = "admin123"
```

## 🖥️ Windows Batch File

Double-click `run.bat` to run tests automatically!

## ❓ Troubleshooting

### Chrome Driver Issues
- The script automatically downloads ChromeDriver
- Make sure Chrome browser is installed
- Check internet connection

### Connection Errors
- Make sure your frontend is running at: `http://20.239.224.248/`
- Check if the URL is accessible in your browser

### Python Not Found
- Make sure Python is installed
- Make sure Python is in PATH
- Try: `python --version` to verify

## 📝 Notes

- All tests interact **only with the frontend**
- No direct backend API calls
- Tests verify frontend behavior and UI interactions
- Screenshots help you see what happened

## ✅ That's All!

Just run `python frontend_tests.py` and you're done!
