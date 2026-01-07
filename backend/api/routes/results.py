"""
API routes for test results and evidence management
"""
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, Any, List
import os

from core.storage import StorageManager
from core.models import AgentExecutionResult

router = APIRouter()
storage = StorageManager()


@router.get("/{execution_id}")
async def get_result(execution_id: str) -> AgentExecutionResult:
    """Get execution result by ID"""
    result = await storage.load_execution_result(execution_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return result


@router.get("/{execution_id}/test-cases")
async def get_test_cases(execution_id: str):
    """Get test cases for an execution"""
    result = await storage.load_execution_result(execution_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "execution_id": execution_id,
        "total_tests": result.total_tests,
        "passed": result.passed_tests,
        "failed": result.failed_tests,
        "skipped": result.skipped_tests,
        "errors": result.error_tests,
        "test_cases": [tc.model_dump() for tc in result.test_cases]
    }


@router.get("/{execution_id}/rca")
async def get_rca(execution_id: str):
    """Get root cause analysis results"""
    result = await storage.load_execution_result(execution_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "execution_id": execution_id,
        "total_issues": len(result.root_cause_analyses),
        "rca_results": [rca.model_dump() for rca in result.root_cause_analyses]
    }


@router.get("/{execution_id}/recommendations")
async def get_recommendations(execution_id: str):
    """Get recommendations for fixing issues"""
    result = await storage.load_execution_result(execution_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "execution_id": execution_id,
        "total_recommendations": len(result.recommendations),
        "recommendations": [rec.model_dump() for rec in result.recommendations]
    }


@router.get("/{execution_id}/evidence")
async def list_evidence(execution_id: str):
    """List all evidence files for an execution"""
    result = await storage.load_execution_result(execution_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "execution_id": execution_id,
        "total_evidence": len(result.evidences),
        "evidences": [ev.model_dump() for ev in result.evidences]
    }


@router.get("/{execution_id}/evidence/{evidence_id}")
async def get_evidence_file(execution_id: str, evidence_id: str):
    """Download a specific evidence file"""
    result = await storage.load_execution_result(execution_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    # Find evidence
    evidence = next(
        (ev for ev in result.evidences if ev.evidence_id == evidence_id),
        None
    )

    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    # Load evidence file
    content = await storage.load_evidence(evidence.file_path)

    if not content:
        raise HTTPException(status_code=404, detail="Evidence file not found")

    return Response(content=content, media_type="application/octet-stream")


@router.get("/{execution_id}/summary")
async def get_execution_summary(execution_id: str):
    """Get execution summary"""
    result = await storage.load_execution_result(execution_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "execution_id": execution_id,
        "agent_type": result.agent_type,
        "status": result.status,
        "duration": result.duration,
        "start_time": result.start_time,
        "end_time": result.end_time,
        "summary": {
            "total_tests": result.total_tests,
            "passed_tests": result.passed_tests,
            "failed_tests": result.failed_tests,
            "skipped_tests": result.skipped_tests,
            "error_tests": result.error_tests,
            "pass_rate": (result.passed_tests / result.total_tests * 100) if result.total_tests > 0 else 0
        },
        "issues": {
            "total_rca": len(result.root_cause_analyses),
            "total_recommendations": len(result.recommendations)
        },
        "evidence": {
            "total_files": len(result.evidences)
        }
    }


@router.delete("/{execution_id}")
async def delete_result(execution_id: str):
    """Delete execution result and associated evidence"""
    success = await storage.delete_execution(execution_id)

    if not success:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "execution_id": execution_id,
        "status": "deleted"
    }


@router.get("/")
async def list_results() -> List[str]:
    """List all stored execution IDs"""
    return storage.list_executions()


@router.get("/stats/storage")
async def get_storage_stats() -> Dict[str, Any]:
    """Get storage statistics"""
    return storage.get_storage_stats()
