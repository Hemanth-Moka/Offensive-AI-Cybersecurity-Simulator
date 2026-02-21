from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database.database import Base

class PasswordAttack(Base):
    __tablename__ = "password_attacks"
    
    id = Column(Integer, primary_key=True, index=True)
    hash_value = Column(String, index=True)
    hash_type = Column(String)  # MD5, SHA256, bcrypt
    cracked = Column(String, nullable=True)
    attack_type = Column(String)  # dictionary, brute_force, hybrid, ai_guided
    attempts = Column(Integer, default=0)
    time_taken = Column(Float)  # seconds
    risk_score = Column(Float)
    pattern_analysis = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PhishingCampaign(Base):
    __tablename__ = "phishing_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    email_subject = Column(String)
    email_body = Column(Text)
    sender_email = Column(String)
    phishing_score = Column(Float)
    urgency_score = Column(Float)
    emotional_manipulation_score = Column(Float)
    suspicious_keywords = Column(JSON)
    click_rate_simulation = Column(Float)
    recommendations = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserBehavior(Base):
    __tablename__ = "user_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    password_pattern = Column(String)
    phishing_susceptibility = Column(Float)
    awareness_level = Column(Float)
    training_recommendations = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class VishingCampaign(Base):
    __tablename__ = "vishing_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    call_script = Column(Text)
    caller_id = Column(String)
    call_duration = Column(Float)  # seconds
    vishing_score = Column(Float)
    urgency_score = Column(Float)
    emotional_manipulation_score = Column(Float)
    social_engineering_tactics = Column(JSON)
    success_rate_simulation = Column(Float)
    suspicious_indicators = Column(JSON)
    recommendations = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
