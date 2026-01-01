from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api import movies, actors, directors, genres

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app with metadata for Swagger documentation
app = FastAPI(
    title="Movie Explorer Platform API",
    description="A comprehensive API for exploring movies, actors, directors, and genres. Built with FastAPI and SQLAlchemy.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Winston",
        "email": "winstondsouza688@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Run seed script on startup
@app.on_event("startup")
async def startup_event():
    """Seed the database on startup if it's empty"""
    import subprocess
    import os
    seed_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "seed_data.py")
    try:
        result = subprocess.run(["python", seed_script], capture_output=True, text=True, check=False)
        print(result.stdout)
        if result.stderr:
            print(f"Seeding warnings/errors: {result.stderr}")
    except Exception as e:
        print(f"Failed to seed database: {e}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router, prefix="/api/movies", tags=["Movies"])
app.include_router(actors.router, prefix="/api/actors", tags=["Actors"])
app.include_router(directors.router, prefix="/api/directors", tags=["Directors"])
app.include_router(genres.router, prefix="/api/genres", tags=["Genres"])

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    """
    Welcome endpoint for the Movie Explorer Platform API.
    """
    return {
        "message": "Welcome to the Movie Explorer Platform API",
        "version": "1.0.0",
        "documentation": "/docs",
        "openapi": "/openapi.json"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "service": "Movie Explorer Platform API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
