from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List, Dict
from app.database.database import get_db
from app.database.models import PhishingCampaign
from app.models.phishing_detector import PhishingSimulator
from app.models.risk_scorer import RiskScorer

router = APIRouter(prefix="/api/phishing", tags=["phishing"])

class EmailAnalysisRequest(BaseModel):
    email_subject: str
    email_body: str
    sender_email: Optional[str] = ""

class CampaignRequest(BaseModel):
    emails: List[Dict]

class PhishingResponse(BaseModel):
    phishing_score: float
    urgency_score: float
    emotional_manipulation_score: float
    suspicious_keywords: List[str]
    click_rate_simulation: float
    recommendations: List[str]
    sender_analysis: Dict
    overall_risk: Dict
    id: Optional[int] = None

@router.post("/analyze", response_model=PhishingResponse)
async def analyze_email(request: EmailAnalysisRequest, db: Session = Depends(get_db)):
    """Analyze an email for phishing indicators"""
    simulator = PhishingSimulator()
    result = simulator.analyze_email(
        request.email_subject,
        request.email_body,
        request.sender_email
    )
    
    # Calculate overall risk
    risk_scorer = RiskScorer()
    overall_risk = risk_scorer.calculate_phishing_risk(result)
    result['overall_risk'] = overall_risk
    
    # Store in database
    db_campaign = PhishingCampaign(
        email_subject=request.email_subject,
        email_body=request.email_body,
        sender_email=request.sender_email,
        phishing_score=result['phishing_score'],
        urgency_score=result['urgency_score'],
        emotional_manipulation_score=result['emotional_manipulation_score'],
        suspicious_keywords=result['suspicious_keywords'],
        click_rate_simulation=result['click_rate_simulation'],
        recommendations=result['recommendations']
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    result['id'] = db_campaign.id
    return PhishingResponse(**result)

@router.post("/campaign")
async def simulate_campaign(request: CampaignRequest, db: Session = Depends(get_db)):
    """Simulate a phishing campaign with multiple emails"""
    simulator = PhishingSimulator()
    campaign_result = simulator.simulate_campaign(request.emails)
    
    # Store individual emails in database
    for email_data in request.emails:
        analysis = simulator.analyze_email(
            email_data.get('subject', ''),
            email_data.get('body', ''),
            email_data.get('sender', '')
        )
        
        db_campaign = PhishingCampaign(
            email_subject=email_data.get('subject', ''),
            email_body=email_data.get('body', ''),
            sender_email=email_data.get('sender', ''),
            phishing_score=analysis['phishing_score'],
            urgency_score=analysis['urgency_score'],
            emotional_manipulation_score=analysis['emotional_manipulation_score'],
            suspicious_keywords=analysis['suspicious_keywords'],
            click_rate_simulation=analysis['click_rate_simulation'],
            recommendations=analysis['recommendations']
        )
        db.add(db_campaign)
    
    db.commit()
    
    return campaign_result

@router.get("/history")
async def get_phishing_history(db: Session = Depends(get_db), limit: int = 50):
    """Get phishing analysis history"""
    campaigns = db.query(PhishingCampaign).order_by(PhishingCampaign.created_at.desc()).limit(limit).all()
    return [
        {
            'id': campaign.id,
            'email_subject': campaign.email_subject,
            'sender_email': campaign.sender_email,
            'phishing_score': campaign.phishing_score,
            'urgency_score': campaign.urgency_score,
            'emotional_manipulation_score': campaign.emotional_manipulation_score,
            'suspicious_keywords': campaign.suspicious_keywords,
            'click_rate_simulation': campaign.click_rate_simulation,
            'recommendations': campaign.recommendations,
            'created_at': campaign.created_at.isoformat() if campaign.created_at else None
        }
        for campaign in campaigns
    ]

@router.get("/stats")
async def get_phishing_stats(db: Session = Depends(get_db)):
    """Get phishing statistics"""
    total_emails = db.query(PhishingCampaign).count()
    high_risk_emails = db.query(PhishingCampaign).filter(PhishingCampaign.phishing_score > 70).count()
    avg_phishing_score = db.query(
        func.avg(PhishingCampaign.phishing_score)
    ).scalar() or 0
    avg_click_rate = db.query(
        func.avg(PhishingCampaign.click_rate_simulation)
    ).scalar() or 0
    
    return {
        'total_emails_analyzed': total_emails,
        'high_risk_emails': high_risk_emails,
        'high_risk_percentage': round((high_risk_emails / total_emails * 100) if total_emails > 0 else 0, 2),
        'average_phishing_score': round(float(avg_phishing_score), 2),
        'average_click_rate': round(float(avg_click_rate), 2)
    }
