"""
Application configuration
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ALGORITHM = "HS256"

# JWT
JWT_TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

# API
API_TITLE = "Offensive AI - Cybersecurity Awareness Platform"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Enterprise cybersecurity awareness and red-team training simulator"

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# Roles
ADMIN_ROLE = "admin"
STUDENT_ROLE = "student"
INSTRUCTOR_ROLE = "instructor"

# Rate limiting
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))

# File upload
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
UPLOAD_DIR = "uploads"
ALLOWED_AUDIO_FORMATS = ["mp3", "wav", "m4a", "ogg", "flac"]

# Environment
environment = os.getenv("ENVIRONMENT", "development")
DEBUG = environment == "development"
