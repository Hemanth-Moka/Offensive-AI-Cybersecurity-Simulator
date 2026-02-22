"""
Authentication API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from database.database import get_db
from database.models import User, UserRole
from app.schemas.schemas import (
    UserRegistration, UserLogin, UserResponse, TokenResponse
)
from app.utils.security import PasswordManager, TokenManager, get_current_user

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegistration, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=PasswordManager.hash_password(user_data.password),
        date_of_birth=user_data.date_of_birth,
        role=UserRole.STUDENT,
        overall_risk_score=100.0,
        awareness_level=0.0,
        training_completed_percentage=0.0,
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create JWT token
    token = TokenManager.create_access_token(
        data={"sub": str(new_user.id), "email": new_user.email, "role": new_user.role.value}
    )
    
    user_response = UserResponse.from_orm(new_user)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_response
    }


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not PasswordManager.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create JWT token
    token = TokenManager.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value}
    )
    
    user_response = UserResponse.from_orm(user)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_response
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user (client-side token deletion)"""
    
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Refresh authentication token"""
    
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create new JWT token
    token = TokenManager.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value}
    )
    
    user_response = UserResponse.from_orm(user)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_response
    }
