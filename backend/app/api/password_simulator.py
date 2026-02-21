from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List, Dict
from app.database.database import get_db
from app.database.models import PasswordAttack
from app.models.password_analyzer import PasswordAttackSimulator
from app.models.risk_scorer import RiskScorer
from app.utils.hash_utils import hash_md5, hash_sha256, hash_bcrypt
from datetime import datetime

router = APIRouter(prefix="/api/password", tags=["password"])

class PasswordHashRequest(BaseModel):
    password: str
    hash_type: str  # MD5, SHA256, bcrypt
    attack_type: str  # dictionary, brute_force, hybrid, ai_guided
    user_metadata: Optional[Dict] = None

class HashOnlyRequest(BaseModel):
    hash_value: str
    hash_type: str
    attack_type: str
    user_metadata: Optional[Dict] = None

class AttackResponse(BaseModel):
    cracked: Optional[str]
    attack_type: str
    attempts: int
    time_taken: float
    risk_score: float
    pattern_analysis: Dict
    overall_risk: Dict
    id: Optional[int] = None

@router.post("/analyze", response_model=AttackResponse)
async def analyze_password(request: PasswordHashRequest, db: Session = Depends(get_db)):
    """Analyze a password by first hashing it, then attempting to crack it"""
    # Hash the password
    if request.hash_type == "MD5":
        hash_value = hash_md5(request.password)
    elif request.hash_type == "SHA256":
        hash_value = hash_sha256(request.password)
    elif request.hash_type == "bcrypt":
        hash_value = hash_bcrypt(request.password)
    else:
        raise HTTPException(status_code=400, detail="Invalid hash type")
    
    # Run attack simulation
    simulator = PasswordAttackSimulator()
    
    if request.attack_type == "dictionary":
        result = simulator.dictionary_attack(hash_value, request.hash_type)
    elif request.attack_type == "brute_force":
        result = simulator.brute_force_attack(hash_value, request.hash_type)
    elif request.attack_type == "hybrid":
        result = simulator.hybrid_attack(hash_value, request.hash_type, request.user_metadata)
    elif request.attack_type == "ai_guided":
        result = simulator.ai_guided_attack(hash_value, request.hash_type, request.user_metadata)
    else:
        raise HTTPException(status_code=400, detail="Invalid attack type")
    
    # Calculate overall risk
    risk_scorer = RiskScorer()
    overall_risk = risk_scorer.calculate_password_risk(result)
    result['overall_risk'] = overall_risk
    
    # Store in database
    db_attack = PasswordAttack(
        hash_value=hash_value,
        hash_type=request.hash_type,
        cracked=result.get('cracked'),
        attack_type=request.attack_type,
        attempts=result['attempts'],
        time_taken=result['time_taken'],
        risk_score=result['risk_score'],
        pattern_analysis=result['pattern_analysis']
    )
    db.add(db_attack)
    db.commit()
    db.refresh(db_attack)
    
    result['id'] = db_attack.id
    return AttackResponse(**result)

@router.post("/crack-hash", response_model=AttackResponse)
async def crack_hash(request: HashOnlyRequest, db: Session = Depends(get_db)):
    """Attempt to crack a provided hash value"""
    simulator = PasswordAttackSimulator()
    
    if request.attack_type == "dictionary":
        result = simulator.dictionary_attack(request.hash_value, request.hash_type)
    elif request.attack_type == "brute_force":
        result = simulator.brute_force_attack(request.hash_value, request.hash_type)
    elif request.attack_type == "hybrid":
        result = simulator.hybrid_attack(request.hash_value, request.hash_type, request.user_metadata)
    elif request.attack_type == "ai_guided":
        result = simulator.ai_guided_attack(request.hash_value, request.hash_type, request.user_metadata)
    else:
        raise HTTPException(status_code=400, detail="Invalid attack type")
    
    # Calculate overall risk
    risk_scorer = RiskScorer()
    overall_risk = risk_scorer.calculate_password_risk(result)
    result['overall_risk'] = overall_risk
    
    # Store in database
    db_attack = PasswordAttack(
        hash_value=request.hash_value,
        hash_type=request.hash_type,
        cracked=result.get('cracked'),
        attack_type=request.attack_type,
        attempts=result['attempts'],
        time_taken=result['time_taken'],
        risk_score=result['risk_score'],
        pattern_analysis=result['pattern_analysis']
    )
    db.add(db_attack)
    db.commit()
    db.refresh(db_attack)
    
    result['id'] = db_attack.id
    return AttackResponse(**result)

@router.get("/history")
async def get_attack_history(db: Session = Depends(get_db), limit: int = 50):
    """Get attack history"""
    attacks = db.query(PasswordAttack).order_by(PasswordAttack.created_at.desc()).limit(limit).all()
    return [
        {
            'id': attack.id,
            'hash_type': attack.hash_type,
            'cracked': attack.cracked,
            'attack_type': attack.attack_type,
            'attempts': attack.attempts,
            'time_taken': attack.time_taken,
            'risk_score': attack.risk_score,
            'pattern_analysis': attack.pattern_analysis,
            'created_at': attack.created_at.isoformat() if attack.created_at else None
        }
        for attack in attacks
    ]

@router.get("/stats")
async def get_attack_stats(db: Session = Depends(get_db)):
    """Get attack statistics"""
    total_attacks = db.query(PasswordAttack).count()
    successful_attacks = db.query(PasswordAttack).filter(PasswordAttack.cracked.isnot(None)).count()
    avg_risk_score = db.query(
        func.avg(PasswordAttack.risk_score)
    ).scalar() or 0
    
    attack_types = db.query(
        PasswordAttack.attack_type,
        func.count(PasswordAttack.id)
    ).group_by(PasswordAttack.attack_type).all()
    
    return {
        'total_attacks': total_attacks,
        'successful_cracks': successful_attacks,
        'success_rate': round((successful_attacks / total_attacks * 100) if total_attacks > 0 else 0, 2),
        'average_risk_score': round(float(avg_risk_score), 2),
        'attacks_by_type': {attack_type: count for attack_type, count in attack_types}
    }
