"""
Security and authentication utilities
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import os

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordManager:
    """Password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storage"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against hashed version"""
        return pwd_context.verify(plain_password, hashed_password)


class TokenManager:
    """JWT token creation and verification"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def verify_token(token: str) -> str:
        """Verify token and return user ID"""
        payload = TokenManager.decode_token(token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        
        return user_id


# HTTP Bearer scheme
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> Dict:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    payload = TokenManager.decode_token(token)
    
    user_id: str = payload.get("sub")
    email: str = payload.get("email")
    role: str = payload.get("role")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    return {
        "user_id": int(user_id),
        "email": email,
        "role": role
    }


def require_role(*roles: str):
    """Dependency to require specific roles"""
    async def role_checker(current_user: Dict = Depends(get_current_user)) -> Dict:
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
    
    return role_checker


class SecurityHeaders:
    """Security headers for responses"""
    
    @staticmethod
    def get_headers() -> Dict[str, str]:
        """Get recommended security headers"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        }


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, identifier: str, max_requests: int = 100, window_seconds: int = 60) -> bool:
        """Check if request is allowed based on rate limit"""
        now = datetime.utcnow()
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove old requests outside window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if (now - req_time).total_seconds() < window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[identifier]) >= max_requests:
            return False
        
        # Add current request
        self.requests[identifier].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()
