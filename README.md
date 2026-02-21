# 🧠 Offensive AI – Adaptive Password & Social Engineering Simulator

## 🎯 Project Overview

An AI-powered cybersecurity platform that simulates password attacks and social engineering campaigns for ethical red-team awareness training. This system demonstrates how attackers exploit weak passwords and human psychology, while providing defensive insights and security awareness feedback.

## ⚠️ Ethical Disclaimer

**This project operates strictly in a controlled lab environment for educational and defensive awareness purposes only. No real-world exploitation or unauthorized testing is permitted.**

## 🛠 Tech Stack

### Frontend
- React.js
- Tailwind CSS
- Chart.js / Recharts (for visualizations)

### Backend
- Python 3.9+
- FastAPI
- Scikit-learn (ML models)
- SQLAlchemy (ORM)
- SQLite (development) / PostgreSQL (production)

## 📁 Project Structure

```
SKILL PALAVER-F/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── password_analyzer.py
│   │   │   ├── phishing_detector.py
│   │   │   ├── vishing_detector.py
│   │   │   └── risk_scorer.py
│   │   ├── api/
│   │   │   ├── password_simulator.py
│   │   │   ├── phishing_simulator.py
│   │   │   └── vishing_simulator.py
│   │   ├── database/
│   │   │   ├── models.py
│   │   │   └── database.py
│   │   └── utils/
│   │       ├── hash_utils.py
│   │       └── ml_utils.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## 🚀 Getting Started

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 📊 Core Features

1. **Adaptive Password Attack Simulator**
   - Dictionary attack simulation
   - Brute-force simulation (limited scope)
   - Hybrid attack patterns
   - AI-guided password guessing
   - Pattern analysis and risk scoring

2. **Social Engineering & Phishing Simulator**
   - AI-based phishing detection
   - Suspicious keyword identification
   - Urgency/emotional manipulation scoring
   - Simulated campaign tracking
   - Personalized awareness recommendations

3. **Voice Phishing (Vishing) Simulator**
   - AI-based vishing detection
   - Social engineering tactics identification
   - Caller ID analysis
   - Urgency/emotional manipulation scoring
   - Success rate simulation
   - Comprehensive security recommendations

## 🔐 Security Notes

- All password hashing is simulated for educational purposes
- No real credentials are stored or processed
- All operations are performed in a controlled lab environment

## 📝 License

Educational use only. See ethical disclaimer above.
