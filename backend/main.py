# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import cases, datasets, environments

# Create FastAPI application
app = FastAPI(
    title="Crypto Test Admin API",
    description="REST API for managing cryptocurrency API test cases",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(cases.router, prefix="/api", tags=["Test Cases"])
app.include_router(datasets.router, prefix="/api", tags=["Data Sets"])
app.include_router(environments.router, prefix="/api", tags=["Environments"])


@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "name": "Crypto Test Admin API",
        "version": "1.0.0",
        "description": "REST API for managing test cases",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "crypto-test-admin-api"
    }
