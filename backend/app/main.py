"""
GymBuddy API - Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth_router, users_router, profiles_router, matches_router, workouts_router

app = FastAPI(
    title="GymBuddy API",
    description="AI-Powered Gym Partner Matching using Collaborative Filtering",
    version="0.1.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(profiles_router)
app.include_router(matches_router)
app.include_router(workouts_router)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to GymBuddy API",
        "version": "0.1.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
