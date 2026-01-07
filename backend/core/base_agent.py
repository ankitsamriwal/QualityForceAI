"""
Base agent class for all testing agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import asyncio
import logging
from datetime import datetime
import uuid

from core.models import (
    AgentMetadata, AgentInput, AgentExecutionResult,
    ExecutionStatus, TestCase, TestEvidence,
    RootCauseAnalysis, Recommendation, AgentType
)


logger = logging.getLogger(__name__)


class BaseTestingAgent(ABC):
    """Base class for all testing agents"""

    def __init__(self):
        self.metadata = self.get_metadata()
        self.execution_id: Optional[str] = None
        self.start_time: Optional[datetime] = None
        self.logs: List[str] = []

    @abstractmethod
    def get_metadata(self) -> AgentMetadata:
        """Return agent metadata"""
        pass

    @abstractmethod
    async def validate_inputs(self, inputs: AgentInput) -> bool:
        """Validate required inputs are provided"""
        pass

    @abstractmethod
    async def generate_test_scripts(self, inputs: AgentInput) -> List[Dict[str, Any]]:
        """Generate test scripts based on inputs"""
        pass

    @abstractmethod
    async def generate_test_data(self, inputs: AgentInput) -> Dict[str, Any]:
        """Generate test data"""
        pass

    @abstractmethod
    async def execute_tests(
        self,
        test_scripts: List[Dict[str, Any]],
        test_data: Dict[str, Any],
        inputs: AgentInput
    ) -> List[TestCase]:
        """Execute generated tests"""
        pass

    @abstractmethod
    async def collect_evidence(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[TestEvidence]:
        """Collect test execution evidence"""
        pass

    @abstractmethod
    async def perform_rca(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[RootCauseAnalysis]:
        """Perform root cause analysis on failures"""
        pass

    @abstractmethod
    async def generate_recommendations(
        self,
        test_cases: List[TestCase],
        rca_results: List[RootCauseAnalysis],
        inputs: AgentInput
    ) -> List[Recommendation]:
        """Generate recommendations based on failures and RCA"""
        pass

    def log(self, message: str, level: str = "INFO"):
        """Add log message"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)

        if level == "ERROR":
            logger.error(message)
        elif level == "WARNING":
            logger.warning(message)
        else:
            logger.info(message)

    async def execute(
        self,
        inputs: AgentInput,
        config: Optional[Dict[str, Any]] = None
    ) -> AgentExecutionResult:
        """
        Main execution method that orchestrates the entire testing process
        """
        self.execution_id = str(uuid.uuid4())
        self.start_time = datetime.now()

        result = AgentExecutionResult(
            execution_id=self.execution_id,
            agent_type=self.metadata.agent_type,
            status=ExecutionStatus.RUNNING,
            start_time=self.start_time
        )

        try:
            self.log(f"Starting {self.metadata.name} execution")

            # Validate inputs
            self.log("Validating inputs")
            if not await self.validate_inputs(inputs):
                raise ValueError("Input validation failed")

            # Generate test scripts
            self.log("Generating test scripts")
            test_scripts = await self.generate_test_scripts(inputs)
            result.test_scripts = test_scripts
            self.log(f"Generated {len(test_scripts)} test scripts")

            # Generate test data
            self.log("Generating test data")
            test_data = await self.generate_test_data(inputs)
            result.test_data = test_data

            # Execute tests
            self.log("Executing tests")
            test_cases = await self.execute_tests(test_scripts, test_data, inputs)
            result.test_cases = test_cases
            result.total_tests = len(test_cases)

            # Calculate test statistics
            from core.models import TestResult
            for tc in test_cases:
                if tc.status == TestResult.PASSED:
                    result.passed_tests += 1
                elif tc.status == TestResult.FAILED:
                    result.failed_tests += 1
                elif tc.status == TestResult.SKIPPED:
                    result.skipped_tests += 1
                elif tc.status == TestResult.ERROR:
                    result.error_tests += 1

            self.log(
                f"Tests completed: {result.passed_tests} passed, "
                f"{result.failed_tests} failed, {result.error_tests} errors"
            )

            # Collect evidence
            self.log("Collecting test evidence")
            evidences = await self.collect_evidence(test_cases, inputs)
            result.evidences = evidences

            # Perform RCA on failures
            if result.failed_tests > 0 or result.error_tests > 0:
                self.log("Performing root cause analysis")
                rca_results = await self.perform_rca(test_cases, inputs)
                result.root_cause_analyses = rca_results

                # Generate recommendations
                self.log("Generating recommendations")
                recommendations = await self.generate_recommendations(
                    test_cases, rca_results, inputs
                )
                result.recommendations = recommendations

            # Mark as completed
            result.status = ExecutionStatus.COMPLETED
            self.log("Execution completed successfully")

        except Exception as e:
            self.log(f"Execution failed: {str(e)}", "ERROR")
            result.status = ExecutionStatus.FAILED
            result.error_message = str(e)

        finally:
            result.end_time = datetime.now()
            result.duration = (result.end_time - result.start_time).total_seconds()
            result.logs = self.logs

        return result

    def calculate_metrics(self, test_cases: List[TestCase]) -> Dict[str, Any]:
        """Calculate various metrics from test execution"""
        total = len(test_cases)
        if total == 0:
            return {}

        from core.models import TestResult
        passed = sum(1 for tc in test_cases if tc.status == TestResult.PASSED)
        failed = sum(1 for tc in test_cases if tc.status == TestResult.FAILED)

        avg_execution_time = sum(
            tc.execution_time for tc in test_cases if tc.execution_time
        ) / total

        return {
            "total_tests": total,
            "pass_rate": (passed / total) * 100,
            "fail_rate": (failed / total) * 100,
            "average_execution_time": avg_execution_time,
        }
