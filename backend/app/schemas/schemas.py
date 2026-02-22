"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserRegistration(BaseModel):
    """User registration schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)
    date_of_birth: Optional[str] = None
    
    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    username: str
    full_name: str
    role: str
    overall_risk_score: float
    awareness_level: float
    training_completed_percentage: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ==================== PASSWORD ANALYSIS SCHEMAS ====================

class PasswordAnalysisRequest(BaseModel):
    """Password analysis request"""
    password: str = Field(..., min_length=1)
    password_hash: Optional[str] = None
    hash_type: Optional[str] = None
    metadata_name: Optional[str] = None
    metadata_dob: Optional[str] = None
    metadata_username: Optional[str] = None
    metadata_interests: Optional[str] = None


class PasswordAnalysisResponse(BaseModel):
    """Password analysis response"""
    strength_score: float
    entropy_score: float
    crack_time_seconds: float
    crack_time_readable: str
    attack_success_probability: float
    behavioral_risk_score: float
    patterns_detected: List[str]
    vulnerability_factors: List[str]
    recommendations: List[str]


class PasswordHistoryItem(BaseModel):
    """Password analysis history item"""
    id: int
    password_input: str
    strength_score: float
    crack_time_readable: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== PHISHING ANALYSIS SCHEMAS ====================

class PhishingAnalysisRequest(BaseModel):
    """Phishing analysis request"""
    email_text: str = Field(..., min_length=10)
    sender_email: Optional[str] = None
    analysis_type: Optional[str] = "email"


class PhishingAnalysisResponse(BaseModel):
    """Phishing analysis response"""
    risk_score: float
    urgency_score: float
    emotional_manipulation_score: float
    social_engineering_tactics: List[str]
    suspicious_indicators: List[str]
    spoofed_domain_detected: bool
    victim_success_rate: float
    recommendations: List[str]
    overall_assessment: str


# ==================== VISHING ANALYSIS SCHEMAS ====================

class VishingAnalysisRequest(BaseModel):
    """Vishing analysis request"""
    call_script: str = Field(..., min_length=10)
    caller_id: Optional[str] = None
    call_duration: float = 0


class CallerAnalysis(BaseModel):
    """Caller analysis details"""
    caller_id: str
    call_duration: float
    suspicious_caller: bool


class VishingAnalysisResponse(BaseModel):
    """Vishing analysis response"""
    vishing_score: float
    urgency_score: float
    emotional_manipulation_score: float
    social_engineering_tactics: List[str]
    suspicious_indicators: List[str]
    caller_analysis: CallerAnalysis
    success_rate_simulation: float
    risk_factors: List[str]
    recommendations: List[str]
    overall_assessment: str


class VishingHistoryItem(BaseModel):
    """Vishing history item"""
    id: int
    call_script: str
    caller_id: Optional[str]
    vishing_score: float
    success_rate_simulation: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== QUIZ SCHEMAS ====================

class QuizQuestion(BaseModel):
    """Quiz question schema"""
    id: int
    text: str
    type: str  # multiple_choice, true_false, etc.
    options: List[str]
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None


class QuizRequest(BaseModel):
    """Quiz request schema"""
    title: str
    description: Optional[str] = None
    category: str
    difficulty: str
    questions: List[QuizQuestion]
    passing_score: float = 70.0


class QuizResponse(BaseModel):
    """Quiz response schema"""
    id: int
    title: str
    description: Optional[str]
    category: str
    difficulty: str
    passing_score: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuizSubmissionRequest(BaseModel):
    """Quiz submission request"""
    quiz_id: int
    answers: Dict[int, str]  # question_id -> answer
    time_taken_seconds: Optional[float] = None


class QuizSubmissionResponse(BaseModel):
    """Quiz submission response"""
    score: float
    passed: bool
    message: str
    answers_review: Optional[Dict[int, Dict[str, Any]]] = None


# ==================== DASHBOARD SCHEMAS ====================

class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_simulations: int
    high_risk_detections: int
    awareness_level: float
    training_completed_percentage: float
    average_password_strength: float
    average_phishing_risk: float
    average_vishing_risk: float
    last_analysis_date: Optional[datetime]


class RiskTrendData(BaseModel):
    """Risk trend data for charts"""
    date: str
    overall_risk: float
    password_risk: float
    phishing_risk: float
    vishing_risk: float


class AnalysisBreakdown(BaseModel):
    """Analysis type breakdown"""
    type: str  # password, phishing, vishing
    count: int
    average_risk: float


class StudentDashboardResponse(BaseModel):
    """Student dashboard response"""
    stats: DashboardStats
    trend_data: List[RiskTrendData]
    analysis_breakdown: List[AnalysisBreakdown]
    recent_quizzes: List[Dict[str, Any]]


class AdminDashboardResponse(BaseModel):
    """Admin dashboard response"""
    total_users: int
    active_users_today: int
    total_simulations: int
    high_risk_users: List[Dict[str, Any]]
    trending_risks: List[str]
    system_health: Dict[str, Any]


# ==================== TRAINING SCHEMAS ====================

class TrainingModule(BaseModel):
    """Training module schema"""
    id: int
    title: str
    description: str
    category: str
    duration_minutes: int
    content: str


class TrainingProgress(BaseModel):
    """Training progress schema"""
    module_id: int
    completion_percentage: float
    last_accessed: datetime
    quiz_passed: Optional[bool] = None


# ==================== ERROR SCHEMAS ====================

class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ValidationError(BaseModel):
    """Validation error schema"""
    field: str
    message: str
