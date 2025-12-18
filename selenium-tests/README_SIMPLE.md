# Simple Selenium Tests - IDURAR ERP CRM

## Quick Start (Windows)

### Step 1: Install Python
- Download Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### Step 2: Install Dependencies
Open Command Prompt or PowerShell and run:
```bash
pip install -r requirements_simple.txt
```

### Step 3: Make Sure Your App is Running
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8888`

### Step 4: Run Tests
```bash
python simple_test.py
```

That's it! The tests will run and save screenshots in the `screenshots/` folder.

## Test Cases

1. **Test 1: Homepage Loads** - Verifies homepage loads successfully
2. **Test 2: Login Functionality** - Tests login with valid credentials
3. **Test 3: API Integration** - Checks frontend-to-backend communication
4. **Test 4: Navigation** - Tests navigation to Invoice page

## Configuration

Edit these values in `simple_test.py` if needed:

```python
BASE_URL = "http://localhost:3000"  # Your frontend URL
API_URL = "http://localhost:8888/api"  # Your backend URL
EMAIL = "admin@admin.com"  # Login email
PASSWORD = "admin123"  # Login password
```

## Screenshots

All screenshots are saved in the `screenshots/` folder:
- `test1_homepage.png` - Homepage test
- `test2_login_page.png` - Login page
- `test2_after_login.png` - After login
- `test3_dashboard.png` - Dashboard
- `test4_invoice_page.png` - Invoice page

## Troubleshooting

### Chrome Driver Issues
The script automatically downloads ChromeDriver. If you have issues:
- Make sure Chrome browser is installed
- Check your internet connection

### Application Not Running
Make sure both frontend and backend are running:
```bash
# Terminal 1 - Backend
cd backend
npm start

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

### Port Issues
If your app runs on different ports, edit `BASE_URL` and `API_URL` in `simple_test.py`

## That's All!

No virtual environments, no complex setup - just run `python simple_test.py`!
