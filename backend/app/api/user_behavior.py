from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List, Dict
from collections import Counter
from app.database.database import get_db
from app.database.models import UserBehavior, PasswordAttack, PhishingCampaign, VishingCampaign
from app.utils.ml_utils import PasswordPatternLearner
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/user-behavior", tags=["user-behavior"])

class UserBehaviorRequest(BaseModel):
    user_id: str
    password_pattern: Optional[str] = None
    phishing_susceptibility: Optional[float] = None
    awareness_level: Optional[float] = None

class UserBehaviorResponse(BaseModel):
    user_id: str
    password_pattern: Optional[str]
    phishing_susceptibility: float
    awareness_level: float
    training_recommendations: List[str]
    behavior_insights: Dict
    risk_profile: Dict

@router.post("/analyze", response_model=UserBehaviorResponse)
async def analyze_user_behavior(request: UserBehaviorRequest, db: Session = Depends(get_db)):
    """Analyze user behavior patterns and generate awareness training recommendations"""
    
    # Get user's historical data
    password_attacks = db.query(PasswordAttack).filter(
        PasswordAttack.pattern_analysis.isnot(None)
    ).order_by(PasswordAttack.created_at.desc()).limit(50).all()
    
    phishing_campaigns = db.query(PhishingCampaign).order_by(
        PhishingCampaign.created_at.desc()
    ).limit(50).all()
    
    vishing_campaigns = db.query(VishingCampaign).order_by(
        VishingCampaign.created_at.desc()
    ).limit(50).all()
    
    # Analyze password patterns
    password_patterns = []
    weak_passwords_count = 0
    avg_password_strength = 0
    
    for attack in password_attacks:
        if attack.pattern_analysis:
            patterns = attack.pattern_analysis.get('patterns_found', [])
            password_patterns.extend(patterns)
            strength = attack.pattern_analysis.get('strength_score', 100)
            avg_password_strength += strength
            if strength < 50:
                weak_passwords_count += 1
    
    if password_attacks:
        avg_password_strength = avg_password_strength / len(password_attacks)
    
    # Analyze phishing susceptibility
    avg_phishing_score = 0
    high_risk_phishing_count = 0
    avg_click_rate = 0
    
    for campaign in phishing_campaigns:
        avg_phishing_score += campaign.phishing_score
        avg_click_rate += campaign.click_rate_simulation
        if campaign.phishing_score > 70:
            high_risk_phishing_count += 1
    
    if phishing_campaigns:
        avg_phishing_score = avg_phishing_score / len(phishing_campaigns)
        avg_click_rate = avg_click_rate / len(phishing_campaigns)
    
    # Analyze vishing susceptibility
    avg_vishing_score = 0
    high_risk_vishing_count = 0
    avg_success_rate = 0
    
    for campaign in vishing_campaigns:
        avg_vishing_score += campaign.vishing_score
        avg_success_rate += campaign.success_rate_simulation
        if campaign.vishing_score > 70:
            high_risk_vishing_count += 1
    
    if vishing_campaigns:
        avg_vishing_score = avg_vishing_score / len(vishing_campaigns)
        avg_success_rate = avg_success_rate / len(vishing_campaigns)
    
    # Calculate awareness level (0-100)
    awareness_score = 100
    awareness_score -= (100 - avg_password_strength) * 0.3
    awareness_score -= avg_phishing_score * 0.3
    awareness_score -= avg_vishing_score * 0.2
    awareness_score -= (weak_passwords_count / max(len(password_attacks), 1)) * 100 * 0.2
    awareness_score = max(0, min(100, awareness_score))
    
    # Calculate phishing susceptibility
    phishing_susceptibility = (avg_phishing_score + avg_click_rate + avg_vishing_score + avg_success_rate) / 4
    
    # Generate training recommendations
    recommendations = []
    
    if avg_password_strength < 50:
        recommendations.append("CRITICAL: Improve password security practices")
        recommendations.append("Attend password security training session")
        recommendations.append("Use password manager to generate strong passwords")
    
    if len(set(password_patterns)) > 3:
        recommendations.append("Multiple weak password patterns detected - review password policies")
    
    if avg_phishing_score > 60:
        recommendations.append("HIGH RISK: Phishing awareness training required")
        recommendations.append("Complete phishing simulation exercises")
        recommendations.append("Learn to identify suspicious email indicators")
    
    if avg_vishing_score > 60:
        recommendations.append("HIGH RISK: Voice phishing awareness training required")
        recommendations.append("Complete vishing simulation exercises")
        recommendations.append("Learn social engineering tactics")
    
    if avg_click_rate > 50:
        recommendations.append("Warning: High click rate on suspicious emails - security awareness needed")
    
    if awareness_score < 50:
        recommendations.append("Comprehensive security awareness training recommended")
        recommendations.append("Regular security assessments advised")
    
    if not recommendations:
        recommendations.append("Good security awareness - maintain current practices")
        recommendations.append("Continue regular security training")
    
    # Behavior insights
    behavior_insights = {
        'common_password_patterns': list(set(password_patterns))[:10],
        'weak_password_ratio': round((weak_passwords_count / max(len(password_attacks), 1)) * 100, 2),
        'average_password_strength': round(avg_password_strength, 2),
        'phishing_risk_level': 'High' if avg_phishing_score > 70 else 'Medium' if avg_phishing_score > 40 else 'Low',
        'vishing_risk_level': 'High' if avg_vishing_score > 70 else 'Medium' if avg_vishing_score > 40 else 'Low',
        'total_analyses': len(password_attacks) + len(phishing_campaigns) + len(vishing_campaigns),
        'high_risk_incidents': high_risk_phishing_count + high_risk_vishing_count
    }
    
    # Risk profile
    risk_profile = {
        'overall_risk': round((100 - awareness_score), 2),
        'password_risk': round(100 - avg_password_strength, 2),
        'phishing_risk': round(avg_phishing_score, 2),
        'vishing_risk': round(avg_vishing_score, 2),
        'risk_level': 'Critical' if awareness_score < 30 else 'High' if awareness_score < 50 else 'Medium' if awareness_score < 70 else 'Low'
    }
    
    # Store or update user behavior
    existing = db.query(UserBehavior).filter(UserBehavior.user_id == request.user_id).first()
    
    if existing:
        existing.password_pattern = request.password_pattern or ','.join(set(password_patterns)[:5])
        existing.phishing_susceptibility = phishing_susceptibility
        existing.awareness_level = awareness_score
        existing.training_recommendations = recommendations
        db.commit()
        db.refresh(existing)
    else:
        new_behavior = UserBehavior(
            user_id=request.user_id,
            password_pattern=request.password_pattern or ','.join(set(password_patterns)[:5]) if password_patterns else None,
            phishing_susceptibility=phishing_susceptibility,
            awareness_level=awareness_score,
            training_recommendations=recommendations
        )
        db.add(new_behavior)
        db.commit()
        db.refresh(new_behavior)
    
    return UserBehaviorResponse(
        user_id=request.user_id,
        password_pattern=request.password_pattern or ','.join(set(password_patterns)[:5]) if password_patterns else None,
        phishing_susceptibility=round(phishing_susceptibility, 2),
        awareness_level=round(awareness_score, 2),
        training_recommendations=recommendations,
        behavior_insights=behavior_insights,
        risk_profile=risk_profile
    )

@router.get("/{user_id}")
async def get_user_behavior(user_id: str, db: Session = Depends(get_db)):
    """Get user behavior analysis"""
    behavior = db.query(UserBehavior).filter(UserBehavior.user_id == user_id).first()
    
    if not behavior:
        raise HTTPException(status_code=404, detail="User behavior not found")
    
    return {
        'user_id': behavior.user_id,
        'password_pattern': behavior.password_pattern,
        'phishing_susceptibility': behavior.phishing_susceptibility,
        'awareness_level': behavior.awareness_level,
        'training_recommendations': behavior.training_recommendations,
        'created_at': behavior.created_at.isoformat() if behavior.created_at else None
    }

@router.get("/stats/overview")
async def get_behavior_stats(db: Session = Depends(get_db)):
    """Get overall behavior statistics"""
    total_users = db.query(UserBehavior).count()
    avg_awareness = db.query(func.avg(UserBehavior.awareness_level)).scalar() or 0
    avg_susceptibility = db.query(func.avg(UserBehavior.phishing_susceptibility)).scalar() or 0
    
    low_awareness = db.query(UserBehavior).filter(UserBehavior.awareness_level < 50).count()
    high_susceptibility = db.query(UserBehavior).filter(UserBehavior.phishing_susceptibility > 70).count()
    
    return {
        'total_users_tracked': total_users,
        'average_awareness_level': round(float(avg_awareness), 2),
        'average_phishing_susceptibility': round(float(avg_susceptibility), 2),
        'low_awareness_users': low_awareness,
        'high_susceptibility_users': high_susceptibility,
        'low_awareness_percentage': round((low_awareness / total_users * 100) if total_users > 0 else 0, 2)
    }
