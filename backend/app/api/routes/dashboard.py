"""
Dashboard API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database.database import get_db
from database.models import (
    User, PasswordAnalysis, PhishingAnalysis, VishingAnalysis, QuizResult
)
from app.utils.security import get_current_user, require_role

router = APIRouter()


@router.get("/student")
async def get_student_dashboard(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student dashboard data"""
    
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get analyses
    password_analyses = db.query(PasswordAnalysis).filter(
        PasswordAnalysis.user_id == current_user["user_id"]
    ).all()
    
    phishing_analyses = db.query(PhishingAnalysis).filter(
        PhishingAnalysis.user_id == current_user["user_id"]
    ).all()
    
    vishing_analyses = db.query(VishingAnalysis).filter(
        VishingAnalysis.user_id == current_user["user_id"]
    ).all()
    
    # Calculate stats
    total_simulations = len(password_analyses) + len(phishing_analyses) + len(vishing_analyses)
    high_risk_count = (
        sum(1 for a in password_analyses if a.strength_score < 40) +
        sum(1 for a in phishing_analyses if a.risk_score >= 70) +
        sum(1 for a in vishing_analyses if a.vishing_score >= 70)
    )
    
    avg_password_strength = (
        sum(a.strength_score for a in password_analyses) / len(password_analyses)
        if password_analyses else 0
    )
    
    avg_phishing_risk = (
        sum(a.risk_score for a in phishing_analyses) / len(phishing_analyses)
        if phishing_analyses else 0
    )
    
    avg_vishing_risk = (
        sum(a.vishing_score for a in vishing_analyses) / len(vishing_analyses)
        if vishing_analyses else 0
    )
    
    return {
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role.value
        },
        "stats": {
            "total_simulations": total_simulations,
            "high_risk_detections": high_risk_count,
            "awareness_level": user.awareness_level,
            "training_completed_percentage": user.training_completed_percentage,
            "overall_risk_score": user.overall_risk_score,
            "average_password_strength": round(avg_password_strength, 2),
            "average_phishing_risk": round(avg_phishing_risk, 2),
            "average_vishing_risk": round(avg_vishing_risk, 2)
        },
        "recent_analyses": {
            "password": [{
                "id": a.id,
                "strength_score": a.strength_score,
                "created_at": a.created_at
            } for a in password_analyses[-5:]],
            "phishing": [{
                "id": a.id,
                "risk_score": a.risk_score,
                "created_at": a.created_at
            } for a in phishing_analyses[-5:]],
            "vishing": [{
                "id": a.id,
                "vishing_score": a.vishing_score,
                "created_at": a.created_at
            } for a in vishing_analyses[-5:]]
        }
    }


@router.get("/admin")
async def get_admin_dashboard(
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get admin dashboard data"""
    
    # Total users
    total_users = db.query(User).count()
    
    # Active users today
    today = datetime.utcnow().date()
    active_today = db.query(User).filter(
        User.last_login >= datetime(today.year, today.month, today.day)
    ).count()
    
    # Total simulations
    total_password = db.query(PasswordAnalysis).count()
    total_phishing = db.query(PhishingAnalysis).count()
    total_vishing = db.query(VishingAnalysis).count()
    total_simulations = total_password + total_phishing + total_vishing
    
    # High risk users
    high_risk_users = db.query(User).filter(User.overall_risk_score >= 70).all()
    
    return {
        "system_metrics": {
            "total_users": total_users,
            "active_users_today": active_today,
            "total_simulations": total_simulations,
            "simulations_breakdown": {
                "password": total_password,
                "phishing": total_phishing,
                "vishing": total_vishing
            }
        },
        "high_risk_users": [{
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "risk_score": u.overall_risk_score,
            "last_login": u.last_login
        } for u in high_risk_users],
        "trending_risks": ["urgency_tactics", "authority_impersonation", "weak_passwords"]
    }
