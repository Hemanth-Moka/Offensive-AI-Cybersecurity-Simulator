from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.api import password_simulator, phishing_simulator, vishing_simulator

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Offensive AI - Cybersecurity Simulator",
    description="AI-powered platform for ethical password attack and social engineering simulation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(password_simulator.router)
app.include_router(phishing_simulator.router)
app.include_router(vishing_simulator.router)

@app.get("/")
async def root():
    return {
        "message": "Offensive AI - Cybersecurity Simulator API",
        "version": "1.0.0",
        "endpoints": {
            "password": "/api/password",
            "phishing": "/api/phishing",
            "vishing": "/api/vishing"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
