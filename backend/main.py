"""
QualityForce AI - Testing Agent Marketplace
Main FastAPI application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from api.routes import agents, executions, results
from core.config import settings
from core.marketplace import AgentMarketplace


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup application resources"""
    # Initialize marketplace
    marketplace = AgentMarketplace()
    app.state.marketplace = marketplace

    yield

    # Cleanup
    await marketplace.shutdown()


app = FastAPI(
    title="QualityForce AI",
    description="Testing Agent Marketplace - AI-Powered Testing Automation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(executions.router, prefix="/api/executions", tags=["executions"])
app.include_router(results.router, prefix="/api/results", tags=["results"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "QualityForce AI",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "agents_available": len(app.state.marketplace.get_all_agents()),
        "active_executions": app.state.marketplace.get_active_execution_count()
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
