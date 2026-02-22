"""
Password analysis API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database.database import get_db
from database.models import PasswordAnalysis, User
from app.schemas.schemas import (
    PasswordAnalysisRequest, PasswordAnalysisResponse, PasswordHistoryItem
)
from app.utils.security import get_current_user
from app.services.ai_scoring_engine import get_scoring_engine

router = APIRouter()


@router.post("/analyze", response_model=PasswordAnalysisResponse)
async def analyze_password(
    request: PasswordAnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze password strength and security
    
    Returns:
    - Strength score (0-100)
    - Entropy score
    - Estimated crack time
    - Detected patterns
    - Vulnerability factors
    - Security recommendations
    """
    
    # Get AI scoring engine
    engine = get_scoring_engine()
    
    # Prepare metadata
    metadata = {
        "name": request.metadata_name,
        "username": request.metadata_username,
        "dob": request.metadata_dob,
        "interests": request.metadata_interests
    }
    
    # Analyze password
    analysis_result = engine.analyze_password(request.password, metadata)
    
    # Save to database
    password_analysis = PasswordAnalysis(
        user_id=current_user["user_id"],
        password_input=request.password[:50],  # Store only hash of password for security
        password_hash=request.password_hash,
        hash_type=request.hash_type,
        metadata_name=request.metadata_name,
        metadata_dob=request.metadata_dob,
        metadata_username=request.metadata_username,
        metadata_interests=request.metadata_interests,
        strength_score=analysis_result["strength_score"],
        entropy_score=analysis_result["entropy_score"],
        crack_time_seconds=analysis_result["crack_time_seconds"],
        attack_success_probability=analysis_result["attack_success_probability"],
        behavioral_risk_score=analysis_result["behavioral_risk_score"],
        patterns_detected=analysis_result["patterns_detected"],
        vulnerability_factors=analysis_result["vulnerability_factors"],
        recommendations=analysis_result["recommendations"],
        created_at=datetime.utcnow()
    )
    
    db.add(password_analysis)
    
    # Update user's risk profile
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if user:
        # Calculate average risk from recent analyses
        recent_analyses = db.query(PasswordAnalysis).filter(
            PasswordAnalysis.user_id == current_user["user_id"]
        ).order_by(PasswordAnalysis.created_at.desc()).limit(10).all()
        
        if recent_analyses:
            avg_risk = sum(a.attack_success_probability for a in recent_analyses) / len(recent_analyses)
            user.overall_risk_score = min(100, avg_risk)
        
        user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return analysis_result


@router.get("/history", response_model=List[PasswordHistoryItem])
async def get_password_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's password analysis history"""
    
    analyses = db.query(PasswordAnalysis).filter(
        PasswordAnalysis.user_id == current_user["user_id"]
    ).order_by(PasswordAnalysis.created_at.desc()).limit(limit).all()
    
    return [PasswordHistoryItem.from_orm(a) for a in analyses]


@router.get("/stats")
async def get_password_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get password analysis statistics"""
    
    analyses = db.query(PasswordAnalysis).filter(
        PasswordAnalysis.user_id == current_user["user_id"]
    ).all()
    
    if not analyses:
        return {
            "total_analyses": 0,
            "average_strength": 0,
            "average_entropy": 0,
            "high_risk_count": 0,
            "patterns_frequency": {}
        }
    
    total = len(analyses)
    avg_strength = sum(a.strength_score for a in analyses) / total
    avg_entropy = sum(a.entropy_score for a in analyses) / total
    high_risk_count = sum(1 for a in analyses if a.strength_score < 40)
    
    # Count pattern frequencies
    pattern_counter = {}
    for a in analyses:
        for pattern in a.patterns_detected:
            pattern_counter[pattern] = pattern_counter.get(pattern, 0) + 1
    
    return {
        "total_analyses": total,
        "average_strength": round(avg_strength, 2),
        "average_entropy": round(avg_entropy, 2),
        "high_risk_count": high_risk_count,
        "patterns_frequency": pattern_counter,
        "trend": "improving" if analyses[-1].strength_score > analyses[0].strength_score else "declining"
    }


@router.post("/crack-hash")
async def crack_hash(
    password_hash: str,
    hash_type: str = "md5",
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Simulate hash cracking (educational purposes only)
    Returns estimated crack time and difficulty
    """
    
    engine = get_scoring_engine()
    
    # This is a simulation - NOT actually cracking hashes
    # Just analyzing the difficulty
    
    # Estimate based on hash algorithm
    hash_difficulty = {
        "md5": 0.5,      # Fast to crack
        "sha1": 0.7,
        "sha256": 1.0,
        "sha512": 1.2,
        "bcrypt": 100.0,  # Very slow
        "argon2": 150.0,   # Very slow
    }
    
    difficulty_multiplier = hash_difficulty.get(hash_type.lower(), 1.0)
    
    # Estimate based on hash length and type
    estimated_crack_time = 365 * 24 * 3600 * difficulty_multiplier  # Years estimation
    
    return {
        "hash_type": hash_type,
        "hash_length": len(password_hash),
        "estimated_crack_time_seconds": estimated_crack_time,
        "crack_time_readable": engine._format_crack_time(estimated_crack_time),
        "difficulty_level": "Very High" if difficulty_multiplier > 50 else "High" if difficulty_multiplier > 1 else "Moderate",
        "message": "This is a SIMULATION only. No actual hashes are being cracked.",
        "security_note": "Modern password hashing (bcrypt, argon2) provides strong protection"
    }
