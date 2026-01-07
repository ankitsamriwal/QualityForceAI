"""
API routes for agent management
"""
from fastapi import APIRouter, HTTPException, Request
from typing import List

from core.models import AgentMetadata, AgentType

router = APIRouter()


@router.get("/", response_model=List[AgentMetadata])
async def list_agents(request: Request):
    """Get list of all available testing agents"""
    marketplace = request.app.state.marketplace
    agents = marketplace.get_all_agents()
    return agents


@router.get("/{agent_type}", response_model=AgentMetadata)
async def get_agent(agent_type: AgentType, request: Request):
    """Get details of a specific agent"""
    marketplace = request.app.state.marketplace
    metadata = marketplace.get_agent_metadata(agent_type)

    if not metadata:
        raise HTTPException(status_code=404, detail=f"Agent {agent_type} not found")

    return metadata
