# Entry point

from fastapi import FastAPI
from app.youtube import router as youtube_router
from app.sentiment import router as sentiment_router
from fastapi.middleware.cors import CORSMiddleware
import logging.config
from app.config import settings, validate_settings, get_cors_origins, get_log_config
import os

# Configure logging
logging.config.dictConfig(get_log_config())
logger = logging.getLogger(__name__)

# Validate configuration on startup
try:
    validate_settings()
    logger.info("Configuration validation passed")
except Exception as e:
    logger.warning(f"Configuration validation issues: {e}")
    # Continue anyway for development

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="API for analyzing YouTube video sentiment and engagement"
)

# Configure CORS - Allow both development and production origins
allowed_origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # React dev server alternative
    "http://127.0.0.1:5173",  # Alternative localhost
    "http://127.0.0.1:3000",  # Alternative localhost for React
    "https://cars-co-za-sentiment-analysis-dashboard.onrender.com",  # Production frontend domain
    "https://yt-senti-dash-4upjjb0ih-tofiek-sasmans-projects.vercel.app",  # Example Vercel domain
    "https://yt-senti-dash.vercel.app",  # Example Vercel domain
]

# Add environment-specific origins
if os.getenv("FRONTEND_URL"):
    allowed_origins.append(os.getenv("FRONTEND_URL"))

# Remove duplicates and filter out None values
allowed_origins = list(set(filter(None, allowed_origins)))

logger.info(f"Allowed CORS origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(youtube_router, prefix="/youtube", tags=["YouTube"])
app.include_router(sentiment_router, prefix="/analyze", tags=["Sentiment"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "cors_origins": len(allowed_origins)
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add a CORS test endpoint for debugging
@app.get("/cors-test")
async def cors_test():
    return {
        "message": "CORS is working!",
        "allowed_origins": allowed_origins
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )