"""
Quiz and training API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from database.database import get_db
from database.models import Quiz, QuizResult, User
from app.schemas.schemas import QuizSubmissionRequest, QuizSubmissionResponse
from app.utils.security import get_current_user

router = APIRouter()


@router.get("/")
async def list_quizzes(
    category: str = None,
    difficulty: str = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List available quizzes"""
    
    query = db.query(Quiz).filter(Quiz.is_active == True)
    
    if category:
        query = query.filter(Quiz.category == category)
    
    if difficulty:
        query = query.filter(Quiz.difficulty == difficulty)
    
    quizzes = query.all()
    
    return [{
        "id": q.id,
        "title": q.title,
        "description": q.description,
        "category": q.category,
        "difficulty": q.difficulty,
        "passing_score": q.passing_score,
        "num_questions": len(q.questions)
    } for q in quizzes]


@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific quiz (without answers)"""
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Remove correct answers from response
    questions = []
    for q in quiz.questions:
        question_data = q.copy() if isinstance(q, dict) else q.__dict__.copy()
        if "correct_answer" in question_data:
            del question_data["correct_answer"]
        questions.append(question_data)
    
    return {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "category": quiz.category,
        "difficulty": quiz.difficulty,
        "passing_score": quiz.passing_score,
        "questions": questions
    }


@router.post("/{quiz_id}/submit", response_model=QuizSubmissionResponse)
async def submit_quiz(
    quiz_id: int,
    request: QuizSubmissionRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit quiz answers"""
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Grade quiz
    correct_count = 0
    total_questions = len(quiz.questions)
    
    for i, question in enumerate(quiz.questions):
        if str(i) in request.answers:
            user_answer = request.answers[str(i)]
            if isinstance(question, dict):
                correct_answer = question.get("correct_answer")
            else:
                correct_answer = question.correct_answer
            
            if user_answer == correct_answer:
                correct_count += 1
    
    score = (correct_count / total_questions * 100) if total_questions > 0 else 0
    passed = score >= quiz.passing_score
    
    # Save result
    result = QuizResult(
        user_id=current_user["user_id"],
        quiz_id=quiz_id,
        score=score,
        passed=passed,
        answers=request.answers,
        time_taken_seconds=request.time_taken_seconds,
        created_at=datetime.utcnow()
    )
    
    db.add(result)
    
    # Update user awareness level
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if user:
        # Update training progress
        if passed:
            user.awareness_level = min(100, user.awareness_level + 5)
        
        user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "score": round(score, 2),
        "passed": passed,
        "message": "Quiz passed!" if passed else f"Quiz failed. Minimum score: {quiz.passing_score}%",
        "correct_answers": correct_count,
        "total_questions": total_questions
    }


@router.get("/results/{quiz_id}")
async def get_quiz_results(
    quiz_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's results for specific quiz"""
    
    results = db.query(QuizResult).filter(
        QuizResult.user_id == current_user["user_id"],
        QuizResult.quiz_id == quiz_id
    ).order_by(QuizResult.created_at.desc()).all()
    
    return [{
        "id": r.id,
        "score": r.score,
        "passed": r.passed,
        "time_taken_seconds": r.time_taken_seconds,
        "created_at": r.created_at
    } for r in results]


@router.get("/progress")
async def get_training_progress(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's training progress"""
    
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get quiz statistics
    all_results = db.query(QuizResult).filter(
        QuizResult.user_id == current_user["user_id"]
    ).all()
    
    passed_quizzes = sum(1 for r in all_results if r.passed)
    total_attempts = len(all_results)
    avg_score = sum(r.score for r in all_results) / total_attempts if all_results else 0
    
    return {
        "awareness_level": user.awareness_level,
        "training_completed_percentage": user.training_completed_percentage,
        "quiz_statistics": {
            "total_attempts": total_attempts,
            "quizzes_passed": passed_quizzes,
            "average_score": round(avg_score, 2),
            "pass_rate": round(passed_quizzes / total_attempts * 100, 2) if total_attempts > 0 else 0
        },
        "recommendations": [
            "Complete more quizzes to improve awareness level",
            "Focus on areas with lower scores",
            "Review security best practices regularly"
        ]
    }
