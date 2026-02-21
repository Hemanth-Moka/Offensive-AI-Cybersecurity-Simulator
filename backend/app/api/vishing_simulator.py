from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List, Dict
from app.database.database import get_db
from app.database.models import VishingCampaign
from app.models.vishing_detector import VishingSimulator
from app.models.risk_scorer import RiskScorer

router = APIRouter(prefix="/api/vishing", tags=["vishing"])

class CallAnalysisRequest(BaseModel):
    call_script: str
    caller_id: Optional[str] = ""
    call_duration: Optional[float] = 0

class CampaignRequest(BaseModel):
    calls: List[Dict]

class VishingResponse(BaseModel):
    vishing_score: float
    urgency_score: float
    emotional_manipulation_score: float
    social_engineering_tactics: List[str]
    suspicious_indicators: List[str]
    success_rate_simulation: float
    recommendations: List[str]
    caller_analysis: Dict
    overall_risk: Dict
    id: Optional[int] = None

@router.post("/analyze", response_model=VishingResponse)
async def analyze_call(request: CallAnalysisRequest, db: Session = Depends(get_db)):
    """Analyze a voice call script for vishing indicators"""
    simulator = VishingSimulator()
    result = simulator.analyze_call(
        request.call_script,
        request.caller_id,
        request.call_duration
    )
    
    # Calculate overall risk
    risk_scorer = RiskScorer()
    overall_risk = risk_scorer.calculate_phishing_risk({
        'phishing_score': result['vishing_score'],
        'urgency_score': result['urgency_score'],
        'emotional_manipulation_score': result['emotional_manipulation_score'],
        'suspicious_keywords': result['suspicious_indicators'],
        'recommendations': result['recommendations']
    })
    result['overall_risk'] = overall_risk
    
    # Store in database
    db_campaign = VishingCampaign(
        call_script=request.call_script,
        caller_id=request.caller_id,
        call_duration=request.call_duration,
        vishing_score=result['vishing_score'],
        urgency_score=result['urgency_score'],
        emotional_manipulation_score=result['emotional_manipulation_score'],
        social_engineering_tactics=result['social_engineering_tactics'],
        success_rate_simulation=result['success_rate_simulation'],
        suspicious_indicators=result['suspicious_indicators'],
        recommendations=result['recommendations']
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    result['id'] = db_campaign.id
    return VishingResponse(**result)

@router.post("/campaign")
async def simulate_campaign(request: CampaignRequest, db: Session = Depends(get_db)):
    """Simulate a vishing campaign with multiple calls"""
    simulator = VishingSimulator()
    campaign_result = simulator.simulate_campaign(request.calls)
    
    # Store individual calls in database
    for call_data in request.calls:
        analysis = simulator.analyze_call(
            call_data.get('script', ''),
            call_data.get('caller_id', ''),
            call_data.get('duration', 0)
        )
        
        db_campaign = VishingCampaign(
            call_script=call_data.get('script', ''),
            caller_id=call_data.get('caller_id', ''),
            call_duration=call_data.get('duration', 0),
            vishing_score=analysis['vishing_score'],
            urgency_score=analysis['urgency_score'],
            emotional_manipulation_score=analysis['emotional_manipulation_score'],
            social_engineering_tactics=analysis['social_engineering_tactics'],
            success_rate_simulation=analysis['success_rate_simulation'],
            suspicious_indicators=analysis['suspicious_indicators'],
            recommendations=analysis['recommendations']
        )
        db.add(db_campaign)
    
    db.commit()
    
    return campaign_result

@router.get("/history")
async def get_vishing_history(db: Session = Depends(get_db), limit: int = 50):
    """Get vishing analysis history"""
    campaigns = db.query(VishingCampaign).order_by(VishingCampaign.created_at.desc()).limit(limit).all()
    return [
        {
            'id': campaign.id,
            'call_script': campaign.call_script[:100] + '...' if len(campaign.call_script) > 100 else campaign.call_script,
            'caller_id': campaign.caller_id,
            'call_duration': campaign.call_duration,
            'vishing_score': campaign.vishing_score,
            'urgency_score': campaign.urgency_score,
            'emotional_manipulation_score': campaign.emotional_manipulation_score,
            'social_engineering_tactics': campaign.social_engineering_tactics,
            'success_rate_simulation': campaign.success_rate_simulation,
            'suspicious_indicators': campaign.suspicious_indicators,
            'recommendations': campaign.recommendations,
            'created_at': campaign.created_at.isoformat() if campaign.created_at else None
        }
        for campaign in campaigns
    ]

@router.get("/stats")
async def get_vishing_stats(db: Session = Depends(get_db)):
    """Get vishing statistics"""
    total_calls = db.query(VishingCampaign).count()
    high_risk_calls = db.query(VishingCampaign).filter(VishingCampaign.vishing_score > 70).count()
    avg_vishing_score = db.query(
        func.avg(VishingCampaign.vishing_score)
    ).scalar() or 0
    avg_success_rate = db.query(
        func.avg(VishingCampaign.success_rate_simulation)
    ).scalar() or 0
    
    return {
        'total_calls_analyzed': total_calls,
        'high_risk_calls': high_risk_calls,
        'high_risk_percentage': round((high_risk_calls / total_calls * 100) if total_calls > 0 else 0, 2),
        'average_vishing_score': round(float(avg_vishing_score), 2),
        'average_success_rate': round(float(avg_success_rate), 2)
    }
