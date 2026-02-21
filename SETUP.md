# Setup Instructions

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend directory (optional, defaults are provided):
```env
DATABASE_URL=sqlite:///./cybersecurity_simulator.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. Run the backend server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Start the backend server first (port 8000)
2. Start the frontend server (port 3000)
3. Open your browser and navigate to `http://localhost:3000`
4. Use the dashboard to:
   - Analyze passwords for security vulnerabilities
   - Simulate password attacks (dictionary, brute-force, hybrid, AI-guided)
   - Analyze emails for phishing indicators
   - View statistics and risk assessments

## Features

### Password Simulator
- Dictionary attack simulation
- Brute-force attack (limited scope for lab)
- Hybrid attack patterns
- AI-guided password guessing
- Pattern analysis and risk scoring

### Phishing Simulator
- AI-based phishing detection
- Suspicious keyword identification
- Urgency/emotional manipulation scoring
- Simulated click-rate prediction
- Personalized security recommendations

## Database

The application uses SQLite by default (for development). The database file will be created automatically on first run.

For production, update the `DATABASE_URL` in `.env` to use PostgreSQL.

## Troubleshooting

### Backend Issues
- Ensure Python 3.9+ is installed
- Check that all dependencies are installed
- Verify the database connection string

### Frontend Issues
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that the backend is running on port 8000
- Verify CORS settings if API calls fail

## Ethical Disclaimer

⚠️ **This project is for educational and defensive awareness purposes only.**
- All operations are performed in a controlled lab environment
- No real-world exploitation or unauthorized testing is permitted
- Use responsibly and only in authorized environments
