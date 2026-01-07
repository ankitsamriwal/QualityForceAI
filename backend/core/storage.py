"""
Storage management for test results and evidence
"""
import os
import json
import shutil
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path
import aiofiles

from core.models import AgentExecutionResult, TestEvidence
from core.config import settings


class StorageManager:
    """Manages storage of test results and evidence files"""

    def __init__(self):
        self.results_dir = Path(settings.RESULTS_DIR)
        self.evidence_dir = Path(settings.EVIDENCE_DIR)

        # Create directories if they don't exist
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    async def save_execution_result(
        self,
        result: AgentExecutionResult
    ) -> str:
        """
        Save execution result to storage.
        Returns the file path.
        """
        # Create execution-specific directory
        execution_dir = self.results_dir / result.execution_id
        execution_dir.mkdir(parents=True, exist_ok=True)

        # Save main result
        result_file = execution_dir / "result.json"
        async with aiofiles.open(result_file, 'w') as f:
            await f.write(result.model_dump_json(indent=2))

        # Save test cases separately
        if result.test_cases:
            test_cases_file = execution_dir / "test_cases.json"
            async with aiofiles.open(test_cases_file, 'w') as f:
                test_cases_data = [tc.model_dump() for tc in result.test_cases]
                await f.write(json.dumps(test_cases_data, indent=2))

        # Save RCA results
        if result.root_cause_analyses:
            rca_file = execution_dir / "rca.json"
            async with aiofiles.open(rca_file, 'w') as f:
                rca_data = [rca.model_dump() for rca in result.root_cause_analyses]
                await f.write(json.dumps(rca_data, indent=2))

        # Save recommendations
        if result.recommendations:
            recommendations_file = execution_dir / "recommendations.json"
            async with aiofiles.open(recommendations_file, 'w') as f:
                rec_data = [rec.model_dump() for rec in result.recommendations]
                await f.write(json.dumps(rec_data, indent=2))

        # Save logs
        logs_file = execution_dir / "execution.log"
        async with aiofiles.open(logs_file, 'w') as f:
            await f.write('\n'.join(result.logs))

        return str(result_file)

    async def load_execution_result(
        self,
        execution_id: str
    ) -> Optional[AgentExecutionResult]:
        """Load execution result from storage"""
        result_file = self.results_dir / execution_id / "result.json"

        if not result_file.exists():
            return None

        async with aiofiles.open(result_file, 'r') as f:
            content = await f.read()
            return AgentExecutionResult.model_validate_json(content)

    async def save_evidence(
        self,
        evidence: TestEvidence,
        content: bytes
    ) -> str:
        """
        Save evidence file.
        Returns the file path.
        """
        # Create evidence directory structure
        evidence_path = self.evidence_dir / evidence.file_path

        # Ensure parent directory exists
        evidence_path.parent.mkdir(parents=True, exist_ok=True)

        # Save evidence file
        async with aiofiles.open(evidence_path, 'wb') as f:
            await f.write(content)

        return str(evidence_path)

    async def load_evidence(
        self,
        file_path: str
    ) -> Optional[bytes]:
        """Load evidence file"""
        evidence_path = self.evidence_dir / file_path

        if not evidence_path.exists():
            return None

        async with aiofiles.open(evidence_path, 'rb') as f:
            return await f.read()

    def list_executions(self) -> List[str]:
        """List all execution IDs"""
        if not self.results_dir.exists():
            return []

        return [
            d.name for d in self.results_dir.iterdir()
            if d.is_dir()
        ]

    async def delete_execution(self, execution_id: str) -> bool:
        """Delete execution results and associated evidence"""
        execution_dir = self.results_dir / execution_id

        if not execution_dir.exists():
            return False

        # Delete execution directory
        shutil.rmtree(execution_dir)
        return True

    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        total_executions = len(self.list_executions())

        # Calculate total size
        total_size = sum(
            f.stat().st_size
            for f in self.results_dir.rglob('*')
            if f.is_file()
        )

        evidence_size = sum(
            f.stat().st_size
            for f in self.evidence_dir.rglob('*')
            if f.is_file()
        )

        return {
            "total_executions": total_executions,
            "results_size_bytes": total_size,
            "evidence_size_bytes": evidence_size,
            "total_size_mb": (total_size + evidence_size) / (1024 * 1024)
        }
