"""
Phishing analysis API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database.database import get_db
from database.models import PhishingAnalysis, User
from app.schemas.schemas import (
    PhishingAnalysisRequest, PhishingAnalysisResponse
)
from app.utils.security import get_current_user
from app.services.ai_scoring_engine import get_scoring_engine

router = APIRouter()


@router.post("/analyze", response_model=PhishingAnalysisResponse)
async def analyze_phishing(
    request: PhishingAnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze email for phishing indicators
    
    Returns:
    - Risk score (0-100)
    - Urgency score
    - Emotional manipulation score
    - Detected social engineering tactics
    - Suspicious indicators
    - Victim success rate
    - Security recommendations
    """
    
    # Get AI scoring engine
    engine = get_scoring_engine()
    
    # Analyze phishing indicators
    analysis_result = engine.analyze_phishing(request.email_text, request.sender_email)
    
    # Save to database
    phishing_analysis = PhishingAnalysis(
        user_id=current_user["user_id"],
        analysis_type=request.analysis_type,
        input_text=request.email_text,
        risk_score=analysis_result["risk_score"],
        urgency_score=analysis_result["urgency_score"],
        emotional_manipulation_score=analysis_result["emotional_manipulation_score"],
        social_engineering_tactics=analysis_result["social_engineering_tactics"],
        suspicious_indicators=analysis_result["suspicious_indicators"],
        spoofed_domain_detected=analysis_result["spoofed_domain_detected"],
        victim_success_rate=analysis_result["victim_success_rate"],
        recommendations=analysis_result["recommendations"],
        created_at=datetime.utcnow()
    )
    
    db.add(phishing_analysis)
    
    # Update user risk profile
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if user:
        # Update awareness level based on detection accuracy
        # Users who identify phishing correctly should have higher awareness
        user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return analysis_result


@router.get("/history", response_model=List[dict])
async def get_phishing_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's phishing analysis history"""
    
    analyses = db.query(PhishingAnalysis).filter(
        PhishingAnalysis.user_id == current_user["user_id"]
    ).order_by(PhishingAnalysis.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": a.id,
            "analysis_type": a.analysis_type,
            "risk_score": a.risk_score,
            "urgency_score": a.urgency_score,
            "emotional_manipulation_score": a.emotional_manipulation_score,
            "social_engineering_tactics": a.social_engineering_tactics,
            "created_at": a.created_at
        }
        for a in analyses
    ]


@router.get("/stats")
async def get_phishing_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get phishing analysis statistics"""
    
    analyses = db.query(PhishingAnalysis).filter(
        PhishingAnalysis.user_id == current_user["user_id"]
    ).all()
    
    if not analyses:
        return {
            "total_analyses": 0,
            "average_risk": 0,
            "high_risk_count": 0,
            "tactics_distribution": {}
        }
    
    total = len(analyses)
    avg_risk = sum(a.risk_score for a in analyses) / total
    high_risk_count = sum(1 for a in analyses if a.risk_score >= 70)
    
    # Count tactic frequencies
    tactics_counter = {}
    for a in analyses:
        for tactic in a.social_engineering_tactics:
            tactics_counter[tactic] = tactics_counter.get(tactic, 0) + 1
    
    return {
        "total_analyses": total,
        "average_risk": round(avg_risk, 2),
        "high_risk_count": high_risk_count,
        "tactics_distribution": tactics_counter,
        "awareness_prediction": "improve" if sum(a.risk_score for a in analyses[-5:]) / len(analyses[-5:]) < avg_risk else "maintain"
    }


@router.post("/campaign")
async def simulate_phishing_campaign(
    campaign_data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Simulate a phishing campaign
    Returns predicted results (educational simulation only)
    """
    
    # This simulates campaign effectiveness based on collected data
    # NOT sending real phishing emails
    
    num_targets = campaign_data.get("number_of_targets", 100)
    email_sophistication = campaign_data.get("sophistication_level", 5)  # 1-10
    
    engine = get_scoring_engine()
    template_email = campaign_data.get("email_template", "")
    
    # Analyze template
    analysis = engine.analyze_phishing(template_email)
    
    # Estimate campaign success based on analysis
    base_success = (analysis["risk_score"] + analysis["victim_success_rate"]) / 2
    sophistication_bonus = (email_sophistication / 10) * 15
    estimated_success_rate = min(100, (base_success + sophistication_bonus) * 0.8)
    
    return {
        "message": "SIMULATION ONLY - No real campaign conducted",
        "num_targets": num_targets,
        "email_analysis": analysis,
        "estimated_success_rate": round(estimated_success_rate, 2),
        "predicted_clicks": round(num_targets * (estimated_success_rate / 100)),
        "predicted_compromised": round(num_targets * (estimated_success_rate / 100) * 0.3),
        "recommendations": [
            "This is an educational simulation",
            "Conducting real phishing campaigns without consent is illegal",
            "Use this data for security awareness training only",
            "Train employees to recognize these tactics"
        ]
    }
