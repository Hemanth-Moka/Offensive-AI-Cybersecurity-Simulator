# 🚀 Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9+ installed
- ✅ Node.js 16+ installed
- ✅ npm or yarn installed

## Quick Setup (5 minutes)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload
```

Backend will run on: **http://localhost:8000**

### 2. Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:3000**

## First Steps

1. **Open Browser:** Navigate to `http://localhost:3000`
2. **Test Password Simulator:**
   - Go to "Password Simulator" tab
   - Enter a weak password like "password123"
   - Select "MD5" hash type
   - Choose "Dictionary Attack"
   - Click "Analyze Password"
   - View the results!

3. **Test Phishing Simulator:**
   - Go to "Phishing Simulator" tab
   - Click "Load Sample Phishing Email"
   - Click "Analyze Email"
   - Review the phishing score and recommendations

4. **View Dashboard:**
   - Go to "Dashboard" tab
   - See statistics and visualizations

## API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Troubleshooting

### Port Already in Use
- Backend: Change port with `uvicorn app.main:app --reload --port 8001`
- Frontend: Update `vite.config.js` port and API proxy

### Module Not Found
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### CORS Errors
- Ensure backend is running before frontend
- Check CORS settings in `backend/app/main.py`

## Next Steps

- Read `PROJECT_DOCUMENTATION.md` for detailed architecture
- Review `SETUP.md` for advanced configuration
- Explore the API endpoints in Swagger UI
- Customize the ML models in `backend/app/utils/ml_utils.py`

## Support

For issues or questions:
1. Check the documentation files
2. Review error messages in console
3. Verify all prerequisites are installed

---

**Remember:** This is for educational purposes only! Use responsibly in controlled environments.
