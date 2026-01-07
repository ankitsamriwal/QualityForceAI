"""
API routes for test execution management
"""
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from typing import Dict, List

from core.models import (
    ExecutionRequest,
    BatchExecutionRequest,
    AgentExecutionResult,
    ExecutionStatus
)
from core.storage import StorageManager

router = APIRouter()
storage = StorageManager()


@router.post("/execute")
async def execute_agent(
    request: Request,
    execution_request: ExecutionRequest
) -> Dict[str, str]:
    """
    Execute a single testing agent.
    Returns execution_id for tracking.
    """
    marketplace = request.app.state.marketplace

    try:
        execution_id = await marketplace.execute_agent(
            agent_type=execution_request.agent_type,
            inputs=execution_request.inputs,
            config=execution_request.config
        )

        return {
            "execution_id": execution_id,
            "status": "started",
            "message": f"Agent {execution_request.agent_type} execution started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute/batch")
async def execute_batch(
    request: Request,
    batch_request: BatchExecutionRequest
) -> Dict[str, Any]:
    """
    Execute multiple testing agents concurrently or sequentially.
    Returns mapping of agent types to execution IDs.
    """
    marketplace = request.app.state.marketplace

    try:
        execution_ids = await marketplace.execute_batch(batch_request)

        return {
            "executions": execution_ids,
            "status": "started",
            "parallel": batch_request.parallel,
            "total_agents": len(execution_ids)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{execution_id}/status")
async def get_execution_status(
    execution_id: str,
    request: Request
) -> Dict[str, str]:
    """Get the status of an execution"""
    marketplace = request.app.state.marketplace
    status = marketplace.get_execution_status(execution_id)

    if status is None:
        raise HTTPException(status_code=404, detail="Execution not found")

    return {
        "execution_id": execution_id,
        "status": status.value
    }


@router.get("/{execution_id}/result", response_model=AgentExecutionResult)
async def get_execution_result(
    execution_id: str,
    request: Request
):
    """Get the full result of an execution"""
    marketplace = request.app.state.marketplace
    result = marketplace.get_execution_result(execution_id)

    if not result:
        # Try loading from storage
        result = await storage.load_execution_result(execution_id)

    if not result:
        raise HTTPException(status_code=404, detail="Execution result not found")

    return result


@router.post("/{execution_id}/cancel")
async def cancel_execution(
    execution_id: str,
    request: Request
) -> Dict[str, str]:
    """Cancel a running execution"""
    marketplace = request.app.state.marketplace

    success = await marketplace.cancel_execution(execution_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Execution not found or already completed"
        )

    return {
        "execution_id": execution_id,
        "status": "cancelled"
    }


@router.get("/")
async def list_executions(request: Request) -> List[AgentExecutionResult]:
    """List all executions"""
    marketplace = request.app.state.marketplace
    return marketplace.get_all_executions()


@router.get("/active/count")
async def get_active_count(request: Request) -> Dict[str, int]:
    """Get count of active executions"""
    marketplace = request.app.state.marketplace
    count = marketplace.get_active_execution_count()

    return {
        "active_executions": count
    }
