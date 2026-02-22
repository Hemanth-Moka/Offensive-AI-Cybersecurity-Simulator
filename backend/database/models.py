"""
SQLAlchemy database models for Offensive AI platform
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"
    INSTRUCTOR = "instructor"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    date_of_birth = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Risk profile
    overall_risk_score = Column(Float, default=0.0)
    awareness_level = Column(Float, default=0.0)
    training_completed_percentage = Column(Float, default=0.0)
    
    # Relationships
    password_analyses = relationship("PasswordAnalysis", back_populates="user")
    phishing_analyses = relationship("PhishingAnalysis", back_populates="user")
    vishing_analyses = relationship("VishingAnalysis", back_populates="user")
    quiz_results = relationship("QuizResult", back_populates="user")
    training_logs = relationship("TrainingLog", back_populates="user")
    
    __repr__ = lambda self: f"<User(id={self.id}, email={self.email}, role={self.role})>"


class PasswordAnalysis(Base):
    __tablename__ = "password_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    password_input = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)
    hash_type = Column(String, nullable=True)  # MD5, SHA256, etc.
    metadata_name = Column(String, nullable=True)
    metadata_dob = Column(String, nullable=True)
    metadata_username = Column(String, nullable=True)
    metadata_interests = Column(String, nullable=True)
    
    # Analysis results
    strength_score = Column(Float, nullable=False)
    entropy_score = Column(Float, nullable=False)
    crack_time_seconds = Column(Float, nullable=False)
    attack_success_probability = Column(Float, nullable=False)
    behavioral_risk_score = Column(Float, nullable=False)
    patterns_detected = Column(JSON, nullable=False, default=list)
    vulnerability_factors = Column(JSON, nullable=False, default=list)
    recommendations = Column(JSON, nullable=False, default=list)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="password_analyses")
    
    __repr__ = lambda self: f"<PasswordAnalysis(id={self.id}, strength={self.strength_score})>"


class PhishingAnalysis(Base):
    __tablename__ = "phishing_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    analysis_type = Column(String, default="email")  # email, message, etc.
    input_text = Column(Text, nullable=False)
    
    # Analysis results
    risk_score = Column(Float, nullable=False)
    urgency_score = Column(Float, nullable=False)
    emotional_manipulation_score = Column(Float, nullable=False)
    social_engineering_tactics = Column(JSON, nullable=False, default=list)
    suspicious_indicators = Column(JSON, nullable=False, default=list)
    spoofed_domain_detected = Column(Boolean, default=False)
    victim_success_rate = Column(Float, nullable=False)
    recommendations = Column(JSON, nullable=False, default=list)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="phishing_analyses")
    
    __repr__ = lambda self: f"<PhishingAnalysis(id={self.id}, risk={self.risk_score})>"


class VishingAnalysis(Base):
    __tablename__ = "vishing_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    call_script = Column(Text, nullable=False)
    caller_id = Column(String, nullable=True)
    call_duration = Column(Float, nullable=False, default=0)
    audio_file_path = Column(String, nullable=True)
    transcript = Column(Text, nullable=True)
    
    # Analysis results
    vishing_score = Column(Float, nullable=False)
    urgency_score = Column(Float, nullable=False)
    emotional_manipulation_score = Column(Float, nullable=False)
    social_engineering_tactics = Column(JSON, nullable=False, default=list)
    suspicious_indicators = Column(JSON, nullable=False, default=list)
    suspicious_caller = Column(Boolean, default=False)
    success_rate_simulation = Column(Float, nullable=False)
    recommendations = Column(JSON, nullable=False, default=list)
    risk_factors = Column(JSON, nullable=False, default=list)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="vishing_analyses")
    
    __repr__ = lambda self: f"<VishingAnalysis(id={self.id}, vishing_score={self.vishing_score})>"


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # password, phishing, vishing, etc.
    difficulty = Column(String, default="medium")  # easy, medium, hard
    questions = Column(JSON, nullable=False)  # Array of question objects
    passing_score = Column(Float, default=70.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    quiz_results = relationship("QuizResult", back_populates="quiz")
    
    __repr__ = lambda self: f"<Quiz(id={self.id}, title={self.title})>"


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)
    answers = Column(JSON, nullable=False)  # User's answers
    time_taken_seconds = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="quiz_results")
    
    __repr__ = lambda self: f"<QuizResult(user={self.user_id}, quiz={self.quiz_id}, score={self.score})>"


class TrainingLog(Base):
    __tablename__ = "training_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    activity_type = Column(String, nullable=False)  # password_analysis, quiz_taken, etc.
    activity_details = Column(JSON, nullable=True)
    risk_score_before = Column(Float, nullable=True)
    risk_score_after = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="training_logs")
    
    __repr__ = lambda self: f"<TrainingLog(user={self.user_id}, activity={self.activity_type})>"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __repr__ = lambda self: f"<AuditLog(id={self.id}, action={self.action})>"


class Dashboard(Base):
    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    total_simulations = Column(Integer, default=0)
    high_risk_detections = Column(Integer, default=0)
    awareness_level = Column(Float, default=0.0)
    last_analysis_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __repr__ = lambda self: f"<Dashboard(user={self.user_id})>"
