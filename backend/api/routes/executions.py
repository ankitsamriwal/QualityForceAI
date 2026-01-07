"""
API routes for test execution management
"""
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from typing import Dict, List, Any

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
        # Validate agent type exists
        if execution_request.agent_type not in marketplace.agents:
            available_agents = ', '.join([str(at.value) for at in marketplace.agents.keys()])
            raise HTTPException(
                status_code=404,
                detail=f"Agent type '{execution_request.agent_type}' not found. Available agents: {available_agents}"
            )

        # Validate inputs are provided
        if not execution_request.inputs:
            raise HTTPException(
                status_code=400,
                detail="Inputs are required for agent execution"
            )

        execution_id = await marketplace.execute_agent(
            agent_type=execution_request.agent_type,
            inputs=execution_request.inputs,
            config=execution_request.config
        )

        return {
            "execution_id": execution_id,
            "status": "started",
            "message": f"Agent {execution_request.agent_type} execution started successfully"
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start execution: {str(e)}"
        )


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
        # Validate batch request
        if not batch_request.executions or len(batch_request.executions) == 0:
            raise HTTPException(
                status_code=400,
                detail="At least one execution is required in batch request"
            )

        # Validate all agent types exist
        invalid_agents = []
        for exec_req in batch_request.executions:
            if exec_req.agent_type not in marketplace.agents:
                invalid_agents.append(str(exec_req.agent_type.value))

        if invalid_agents:
            raise HTTPException(
                status_code=404,
                detail=f"Invalid agent types: {', '.join(invalid_agents)}"
            )

        execution_ids = await marketplace.execute_batch(batch_request)

        return {
            "executions": execution_ids,
            "status": "started",
            "parallel": batch_request.parallel,
            "total_agents": len(execution_ids),
            "message": f"Successfully started {len(execution_ids)} agent execution(s)"
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start batch execution: {str(e)}"
        )


@router.get("/{execution_id}/status")
async def get_execution_status(
    execution_id: str,
    request: Request
) -> Dict[str, str]:
    """Get the status of an execution"""
    marketplace = request.app.state.marketplace
    status = marketplace.get_execution_status(execution_id)

    if status is None:
        raise HTTPException(
            status_code=404,
            detail=f"Execution '{execution_id}' not found"
        )

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
        raise HTTPException(
            status_code=404,
            detail=f"Execution result for '{execution_id}' not found"
        )

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
            detail=f"Execution '{execution_id}' not found or already completed"
        )

    return {
        "execution_id": execution_id,
        "status": "cancelled",
        "message": "Execution cancelled successfully"
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
