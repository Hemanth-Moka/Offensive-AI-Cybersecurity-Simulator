# Offensive AI - Cybersecurity Awareness Platform

## 🎯 Overview

**Offensive AI** is an enterprise-grade, production-ready cybersecurity awareness and red-team training simulator. It provides realistic, algorithm-guided simulations for password attacks, phishing campaigns, and vishing (voice phishing) scenarios—all within a controlled, educational environment.

**⚠️ CRITICAL DISCLAIMER:**
This system is **STRICTLY FOR AUTHORIZED EDUCATIONAL AND RED-TEAM TRAINING ONLY**. It does NOT perform real attacks, real password cracking, or real unauthorized access. All simulations are mathematical and behavioral. Unauthorized use against systems you don't own is illegal.

## 📋 Features

### ✅ Core Modules

#### 1. **Adaptive Password Attack Simulator**
- Dictionary attack simulation
- Brute-force simulation with time estimation
- AI-guided guess generation using metadata
- Pattern detection (sequential, keyboard walks, repetitive)
- Entropy & complexity scoring (0-100)
- Behavioral risk assessment
- Real-time strength analysis

#### 2. **Email Phishing Detector**
- Urgency language detection
- Fear-based manipulation analysis
- Authority impersonation detection
- Spoofed domain detection
- Emotional manipulation scoring
- Victim success probability estimation

#### 3. **Voice Phishing (Vishing) Simulator**
- AI-powered script analysis
- Audio file transcription (MP3, WAV, M4A)
- Caller ID analysis & spoofing detection
- Urgency & emotional manipulation scoring
- Social engineering tactics detection
- Real-time threat assessment

#### 4. **Dashboard & Analytics**
- Real-time risk scoring
- Historical trend analysis
- Performance metrics
- User awareness levels
- Personalized recommendations

#### 5. **Training & Quiz Module**
- Scenario-based security quizzes
- Phishing identification challenges
- Progress tracking
- Completion certifications

#### 6. **Admin Dashboard**
- System-wide analytics
- High-risk user identification
- Audit trails

## 🏗️ Architecture

```
Offensive AI Platform
├── Backend (FastAPI)
│   ├── AI Scoring Engine
│   ├── Database Models
│   ├── Authentication & Security
│   ├── REST API Routes
│   └── Services Layer
├── Frontend (React + Vite)
│   ├── Simulators
│   ├── Dashboard
│   └── Training Module
└── Database (SQLite / PostgreSQL)
```

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/offensive-ai.git
cd offensive-ai

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Manual Setup (Development)

#### Backend Setup
```bash
python -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📚 API Endpoints

### Authentication
```http
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/refresh
```

### Password Analysis
```http
POST /api/password/analyze
GET  /api/password/history
GET  /api/password/stats
```

### Phishing Analysis
```http
POST /api/phishing/analyze
GET  /api/phishing/history
GET  /api/phishing/stats
```

### Vishing Analysis
```http
POST /api/vishing/analyze
POST /api/vishing/transcribe
GET  /api/vishing/history
GET  /api/vishing/stats
```

### Dashboard
```http
GET /api/dashboard/student
GET /api/dashboard/admin
```

### Quiz
```http
GET  /api/quiz
POST /api/quiz/{quiz_id}/submit
GET  /api/quiz/progress
```

## 🔐 Security Features

- ✅ JWT Authentication
- ✅ Role-based access control
- ✅ Password hashing (bcrypt)
- ✅ CORS security
- ✅ Rate limiting
- ✅ Input validation (Pydantic)
- ✅ SQL injection prevention
- ✅ Audit logging
- ✅ HTTPS ready

## 📊 Database Schema

Key tables:
- `users` - User accounts
- `password_analyses` - Password history
- `phishing_analyses` - Email analysis
- `vishing_analyses` - Voice analysis
- `quizzes` - Training quizzes
- `quiz_results` - User results
- `audit_logs` - Security trail

## 🧪 Testing

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

## 🐳 Docker Commands

```bash
docker-compose up -d           # Start
docker-compose down            # Stop
docker-compose logs -f backend # View logs
docker-compose exec backend bash  # Shell access
```

## 📝 API Example

```python
from app.services.ai_scoring_engine import get_scoring_engine

engine = get_scoring_engine()
result = engine.analyze_password("MyP@ssw0rd!")

print(f"Strength: {result['strength_score']}")
print(f"Crack time: {result['crack_time_readable']}")
```

## ⚖️ Legal Notice

**DISCLAIMER:** This tool is for authorized cybersecurity training ONLY. Unauthorized use is ILLEGAL.

## 👥 Support

- GitHub Issues: [Report bugs](https://github.com/yourproject/issues)
- Docs: [Full documentation](./docs)
- Email: security@yourorganization.com

---

**Made with ❤️ for cybersecurity awareness** | Version 1.0.0
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
