"""
Vishing (Voice Phishing) analysis API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import os
import shutil

from database.database import get_db
from database.models import VishingAnalysis, User
from app.schemas.schemas import (
    VishingAnalysisRequest, VishingAnalysisResponse, VishingHistoryItem
)
from app.utils.security import get_current_user
from app.services.ai_scoring_engine import get_scoring_engine
from config import UPLOAD_DIR, ALLOWED_AUDIO_FORMATS, MAX_UPLOAD_SIZE

router = APIRouter()


@router.post("/analyze", response_model=VishingAnalysisResponse)
async def analyze_vishing(
    request: VishingAnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze call script for vishing indicators
    
    Returns:
    - Vishing risk score (0-100)
    - Urgency and emotional manipulation scores
    - Detected social engineering tactics
    - Caller analysis
    - Success rate simulation
    - Security recommendations
    """
    
    # Get AI scoring engine
    engine = get_scoring_engine()
    
    # Analyze vishing script
    analysis_result = engine.analyze_vishing(
        request.call_script,
        request.caller_id,
        request.call_duration
    )
    
    # Save to database
    vishing_analysis = VishingAnalysis(
        user_id=current_user["user_id"],
        call_script=request.call_script,
        caller_id=request.caller_id,
        call_duration=request.call_duration,
        vishing_score=analysis_result["vishing_score"],
        urgency_score=analysis_result["urgency_score"],
        emotional_manipulation_score=analysis_result["emotional_manipulation_score"],
        social_engineering_tactics=analysis_result["social_engineering_tactics"],
        suspicious_indicators=analysis_result["suspicious_indicators"],
        suspicious_caller=analysis_result["caller_analysis"]["suspicious_caller"],
        success_rate_simulation=analysis_result["success_rate_simulation"],
        recommendations=analysis_result["recommendations"],
        risk_factors=analysis_result["risk_factors"],
        created_at=datetime.utcnow()
    )
    
    db.add(vishing_analysis)
    
    # Update user risk profile
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if user:
        # Calculate average vishing risk
        all_vishing = db.query(VishingAnalysis).filter(
            VishingAnalysis.user_id == current_user["user_id"]
        ).all()
        
        if all_vishing:
            avg_vishing_risk = sum(v.vishing_score for v in all_vishing) / len(all_vishing)
            user.overall_risk_score = max(user.overall_risk_score, avg_vishing_risk * 0.3)
        
        user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return analysis_result


@router.post("/transcribe")
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Transcribe audio file to text
    
    Supported formats: mp3, wav, m4a, ogg, flac
    Max file size: 50MB
    
    Returns:
    - Transcript text
    - Confidence score
    - Language detected
    """
    
    # Validate file format
    file_extension = audio_file.filename.split('.')[-1].lower()
    
    if file_extension not in ALLOWED_AUDIO_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported audio format. Allowed: {', '.join(ALLOWED_AUDIO_FORMATS)}"
        )
    
    # Check file size
    file_size = await audio_file.seek(0, 2)
    if file_size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {MAX_UPLOAD_SIZE // (1024*1024)}MB limit"
        )
    
    await audio_file.seek(0)
    
    # Create upload directory if doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Save file temporarily
    file_path = os.path.join(UPLOAD_DIR, f"{current_user['user_id']}_{audio_file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            contents = await audio_file.read()
            buffer.write(contents)
        
        # TODO: Integrate with actual speech-to-text service
        # Options:
        # - Google Cloud Speech-to-Text
        # - AWS Transcribe
        # - Azure Speech Services
        # - OpenAI Whisper API
        # - Local: Vosk, SpeechRecognition
        
        # For now, return placeholder response
        # In production, implement real transcription
        
        transcript = """
        [This is a placeholder transcript. In production, integrate with speech-to-text service]
        
        Hello, this is a call from your bank regarding suspicious activity. 
        We need you to verify your account information immediately.
        Please provide your account number and PIN to confirm your identity.
        """
        
        return {
            "transcript": transcript.strip(),
            "confidence": 0.92,
            "language": "en-US",
            "duration_seconds": 45,
            "message": "For production use, integrate with speech-to-text API (Google Cloud, AWS, Azure, Whisper, etc.)"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transcription error: {str(e)}"
        )
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


@router.get("/history", response_model=List[VishingHistoryItem])
async def get_vishing_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's vishing analysis history"""
    
    analyses = db.query(VishingAnalysis).filter(
        VishingAnalysis.user_id == current_user["user_id"]
    ).order_by(VishingAnalysis.created_at.desc()).limit(limit).all()
    
    return [VishingHistoryItem.from_orm(a) for a in analyses]


@router.get("/stats")
async def get_vishing_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get vishing analysis statistics"""
    
    analyses = db.query(VishingAnalysis).filter(
        VishingAnalysis.user_id == current_user["user_id"]
    ).all()
    
    if not analyses:
        return {
            "total_analyses": 0,
            "average_risk": 0,
            "high_risk_count": 0,
            "tactics_distribution": {}
        }
    
    total = len(analyses)
    avg_risk = sum(a.vishing_score for a in analyses) / total
    high_risk_count = sum(1 for a in analyses if a.vishing_score >= 70)
    
    # Count tactic frequencies
    tactics_counter = {}
    for a in analyses:
        for tactic in a.social_engineering_tactics:
            tactics_counter[tactic] = tactics_counter.get(tactic, 0) + 1
    
    # Average success rate
    avg_success_rate = sum(a.success_rate_simulation for a in analyses) / total
    
    return {
        "total_analyses": total,
        "average_risk": round(avg_risk, 2),
        "average_success_rate": round(avg_success_rate, 2),
        "high_risk_count": high_risk_count,
        "tactics_distribution": tactics_counter,
        "trend": "improving" if analyses[-1].vishing_score < analyses[0].vishing_score else "declining"
    }


@router.post("/campaign")
async def simulate_vishing_campaign(
    campaign_data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Simulate a vishing campaign
    Returns predicted effectiveness (educational simulation only)
    """
    
    # This simulates campaign effectiveness
    # NOT making real calls
    
    num_targets = campaign_data.get("number_of_targets", 100)
    sophistication = campaign_data.get("sophistication_level", 5)  # 1-10
    
    engine = get_scoring_engine()
    script = campaign_data.get("call_script", "")
    caller_id = campaign_data.get("caller_id", "")
    
    # Analyze script
    analysis = engine.analyze_vishing(script, caller_id, 0)
    
    # Estimate success
    base_success = (analysis["vishing_score"] * 0.7 + analysis["success_rate_simulation"] * 0.3)
    sophistication_bonus = (sophistication / 10) * 10
    estimated_success_rate = min(100, base_success + sophistication_bonus)
    
    return {
        "message": "SIMULATION ONLY - No real vishing campaign conducted",
        "num_targets": num_targets,
        "script_analysis": analysis,
        "estimated_success_rate": round(estimated_success_rate, 2),
        "predicted_victims": round(num_targets * (estimated_success_rate / 100)),
        "predicted_data_compromised": round(num_targets * (estimated_success_rate / 100) * 0.4),
        "recommendations": [
            "This is an educational simulation only",
            "Unauthorized vishing is illegal and unethical",
            "Use this data for employee training and awareness",
            "Report actual vishing attempts to authorities"
        ]
    }
