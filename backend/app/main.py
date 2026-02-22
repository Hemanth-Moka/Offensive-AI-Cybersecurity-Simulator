"""
Main FastAPI application for Offensive AI Platform
"""
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

from config import (
    API_TITLE, API_VERSION, API_DESCRIPTION,
    ALLOWED_ORIGINS, DEBUG, environment
)
from database.database import init_db
from app.api.password_simulator import router as password_router
from app.api.phishing_simulator import router as phishing_router
from app.api.vishing_simulator import router as vishing_router
from app.api.user_behavior import router as behavior_router
from app.database.database import Base as AppBase, engine as app_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    openapi_url="/api/openapi.json" if DEBUG else None,
    docs_url="/api/docs" if DEBUG else None,
    redoc_url="/api/redoc" if DEBUG else None,
)

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_db()
        AppBase.metadata.create_all(bind=app_engine)
        logger.info(f"Application started in {environment} mode")
        logger.info(f"CORS allowed origins: {ALLOWED_ORIGINS}")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down...")


# Health check endpoint
@app.get("/api/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": environment,
        "version": API_VERSION
    }


# API info endpoint
@app.get("/api/info", status_code=status.HTTP_200_OK)
async def api_info():
    """API information endpoint"""
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "environment": environment,
        "docs_url": "/api/docs" if DEBUG else None
    }


# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error" if not DEBUG else str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Offensive AI - Cybersecurity Awareness Platform",
        "api_version": API_VERSION,
        "documentation": "/api/docs",
        "health": "/api/health"
    }


# API routers
app.include_router(password_router)
app.include_router(phishing_router)
app.include_router(vishing_router)
app.include_router(behavior_router)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG,
        log_level="info"
    )
