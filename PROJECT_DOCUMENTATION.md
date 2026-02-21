# 🧠 Offensive AI – Adaptive Password & Social Engineering Simulator
## Capstone Project Documentation

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Core Modules](#core-modules)
4. [AI/ML Components](#aiml-components)
5. [API Endpoints](#api-endpoints)
6. [Frontend Components](#frontend-components)
7. [Database Schema](#database-schema)
8. [Security Considerations](#security-considerations)
9. [Ethical Considerations](#ethical-considerations)
10. [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

This project is an AI-powered cybersecurity platform designed for ethical red-team awareness training. It simulates password attacks and social engineering campaigns in a controlled environment to help organizations understand vulnerabilities and improve security awareness.

### Key Objectives
- Demonstrate how attackers exploit weak passwords
- Simulate social engineering and phishing tactics
- Provide defensive insights and security awareness feedback
- Measure vulnerability through risk scoring

---

## 🏗 Architecture

### Technology Stack

**Backend:**
- Python 3.9+
- FastAPI (REST API framework)
- SQLAlchemy (ORM)
- SQLite/PostgreSQL (Database)
- Scikit-learn (ML models)
- NLTK (Natural Language Processing)

**Frontend:**
- React.js 18
- Tailwind CSS (Styling)
- Recharts (Data visualization)
- Axios (HTTP client)
- Vite (Build tool)

### System Architecture

```
┌─────────────────┐
│   React Frontend │
│   (Port 3000)    │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI Backend│
│   (Port 8000)    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│ SQLite │ │ ML Models│
│   DB   │ │ (Pattern │
└────────┘ │ Learning)│
           └──────────┘
```

---

## 🔧 Core Modules

### 1. Password Attack Simulator

**Location:** `backend/app/models/password_analyzer.py`

**Features:**
- Dictionary attack simulation
- Brute-force attack (limited to 4 characters, 1000 attempts max)
- Hybrid attack (combines dictionary + AI guesses)
- AI-guided attack (uses pattern learning)

**Attack Types:**
1. **Dictionary Attack:** Uses common password lists
2. **Brute Force:** Systematic character combination (limited scope)
3. **Hybrid Attack:** Combines dictionary with AI-generated guesses
4. **AI-Guided Attack:** Uses user metadata to generate intelligent guesses

**Output:**
- Cracked password (if successful)
- Number of attempts
- Time taken
- Risk score (0-100)
- Pattern analysis

### 2. Social Engineering & Phishing Simulator

**Location:** `backend/app/models/phishing_detector.py`

**Features:**
- AI-based phishing detection
- Suspicious keyword identification
- Urgency scoring
- Emotional manipulation detection
- Click-rate simulation

**Analysis Components:**
- Phishing score (0-100)
- Urgency indicators
- Emotional manipulators
- Sender domain analysis
- Keyword detection

**Output:**
- Phishing likelihood score
- Click-rate simulation
- Personalized recommendations
- Risk factors

### 3. Risk Scorer

**Location:** `backend/app/models/risk_scorer.py`

**Functionality:**
- Calculates comprehensive risk scores
- Provides security recommendations
- Categorizes risk levels (Critical, High, Medium, Low, Very Low)
- Identifies risk factors

---

## 🤖 AI/ML Components

### Password Pattern Learner

**Location:** `backend/app/utils/ml_utils.py`

**Capabilities:**
- Detects common password patterns:
  - Sequential patterns (123, abc, qwerty)
  - Repetitive characters
  - Keyboard walks
  - Date patterns
  - Name patterns
  - Common words

**Pattern Analysis:**
- Strength scoring (0-100)
- Complexity assessment
- Length evaluation
- Character variety check

**AI-Guided Guessing:**
- Uses user metadata (name, DOB) to generate personalized guesses
- Prioritizes common patterns
- Combines multiple attack vectors

### Phishing Detector

**Location:** `backend/app/utils/ml_utils.py`

**Detection Methods:**
- Keyword-based analysis
- Urgency indicator scoring
- Emotional manipulation detection
- Domain spoofing detection
- Pattern recognition

**Scoring Algorithm:**
```
Phishing Score = 
  (Suspicious Keywords × 10) +
  (Urgency Score × 0.3) +
  (Emotional Score × 0.3) +
  (Sender Analysis Score)
```

---

## 🌐 API Endpoints

### Password Simulator Endpoints

**Base URL:** `/api/password`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze` | Analyze a password by hashing and attempting to crack it |
| POST | `/crack-hash` | Attempt to crack a provided hash value |
| GET | `/history` | Get attack history (limit: 50) |
| GET | `/stats` | Get attack statistics |

**Request Example (Analyze):**
```json
{
  "password": "password123",
  "hash_type": "MD5",
  "attack_type": "dictionary",
  "user_metadata": {
    "name": "John",
    "dob": "1990-01-01"
  }
}
```

### Phishing Simulator Endpoints

**Base URL:** `/api/phishing`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze` | Analyze an email for phishing indicators |
| POST | `/campaign` | Simulate a phishing campaign with multiple emails |
| GET | `/history` | Get analysis history (limit: 50) |
| GET | `/stats` | Get phishing statistics |

**Request Example (Analyze):**
```json
{
  "email_subject": "URGENT: Account Suspension",
  "email_body": "Click here to verify...",
  "sender_email": "security@bank.com"
}
```

---

## 🎨 Frontend Components

### Dashboard (`components/Dashboard.jsx`)
- Overview statistics
- Attack type distribution charts
- Risk level visualization
- Key metrics display

### Password Simulator (`components/PasswordSimulator.jsx`)
- Password analysis form
- Hash cracking form
- Results display with risk assessment
- Pattern analysis visualization
- Attack history table

### Phishing Simulator (`components/PhishingSimulator.jsx`)
- Email analysis form
- Sample email loader
- Phishing score visualization
- Keyword highlighting
- Recommendations display
- Analysis history

---

## 💾 Database Schema

### PasswordAttack Table
```sql
- id: Integer (Primary Key)
- hash_value: String
- hash_type: String (MD5, SHA256, bcrypt)
- cracked: String (Nullable)
- attack_type: String
- attempts: Integer
- time_taken: Float
- risk_score: Float
- pattern_analysis: JSON
- created_at: DateTime
```

### PhishingCampaign Table
```sql
- id: Integer (Primary Key)
- email_subject: String
- email_body: Text
- sender_email: String
- phishing_score: Float
- urgency_score: Float
- emotional_manipulation_score: Float
- suspicious_keywords: JSON
- click_rate_simulation: Float
- recommendations: JSON
- created_at: DateTime
```

### UserBehavior Table
```sql
- id: Integer (Primary Key)
- user_id: String
- password_pattern: String
- phishing_susceptibility: Float
- awareness_level: Float
- training_recommendations: JSON
- created_at: DateTime
```

---

## 🔐 Security Considerations

### Hash Simulation
- All password hashing is **simulated** for educational purposes
- MD5, SHA256, and bcrypt implementations are for demonstration only
- No real credentials are stored or processed

### Data Protection
- Database stores only simulation results
- No actual user passwords or sensitive data
- All operations are performed in a controlled lab environment

### API Security
- CORS configured for development
- Input validation on all endpoints
- Error handling to prevent information leakage

---

## ⚖️ Ethical Considerations

### Scope Limitations
1. **Lab Environment Only:** All operations must be performed in controlled environments
2. **Educational Purpose:** Designed for security awareness training
3. **No Real Exploitation:** No unauthorized testing or real-world attacks
4. **Defensive Focus:** Primary goal is to improve security awareness

### Responsible Use Guidelines
- Use only in authorized environments
- Obtain proper permissions before testing
- Do not use against real systems without authorization
- Respect privacy and data protection laws
- Report vulnerabilities responsibly

### Disclaimer
This project is for **educational and defensive awareness purposes only**. Users are responsible for ensuring all activities comply with applicable laws and regulations.

---

## 🚀 Future Enhancements

### Potential Improvements
1. **Enhanced ML Models:**
   - Deep learning for password pattern recognition
   - NLP models for better phishing detection
   - Behavioral analysis models

2. **Additional Features:**
   - Multi-factor authentication simulation
   - Social media phishing detection
   - Voice phishing (vishing) analysis
   - SMS phishing (smishing) detection

3. **User Management:**
   - User authentication and authorization
   - Role-based access control
   - Training progress tracking

4. **Reporting:**
   - PDF report generation
   - Customizable dashboards
   - Export capabilities

5. **Integration:**
   - SIEM integration
   - Security awareness platform integration
   - API for third-party tools

---

## 📊 Methodology

### Password Attack Simulation
1. Hash the input password using specified algorithm
2. Run selected attack type (dictionary, brute-force, hybrid, AI-guided)
3. Analyze patterns if password is cracked
4. Calculate risk score based on:
   - Password strength
   - Attack complexity
   - Time taken
   - Number of attempts

### Phishing Detection
1. Extract text from email subject and body
2. Identify suspicious keywords
3. Calculate urgency and emotional manipulation scores
4. Analyze sender domain
5. Generate phishing likelihood score
6. Simulate click rate based on score
7. Provide personalized recommendations

---

## 📝 Conclusion

This project successfully demonstrates:
- How attackers exploit weak passwords
- Social engineering tactics and detection
- AI-powered security analysis
- Risk assessment and scoring
- Security awareness training capabilities

The platform provides valuable insights for organizations to improve their cybersecurity posture through awareness and education.

---

## 📚 References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Documentation: https://react.dev/
- OWASP Password Guidelines
- NIST Cybersecurity Framework
- Social Engineering Attack Patterns

---

**Project Version:** 1.0.0  
**Last Updated:** 2024  
**License:** Educational Use Only
