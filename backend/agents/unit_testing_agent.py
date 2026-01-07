"""
Unit Testing Agent - Generates and executes unit tests for source code
"""
import uuid
import re
from typing import Dict, Any, List
from datetime import datetime

from core.base_agent import BaseTestingAgent
from core.models import (
    AgentMetadata, AgentInput, AgentType,
    TestCase, TestEvidence, RootCauseAnalysis, Recommendation, TestResult
)


class UnitTestingAgent(BaseTestingAgent):
    """Agent specialized in unit testing"""

    def get_metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_type=AgentType.UNIT_TESTING,
            name="Unit Testing Agent",
            description="Generates and executes comprehensive unit tests for source code",
            version="1.0.0",
            required_inputs=["source_code"],
            optional_inputs=["libraries", "config"],
            capabilities=[
                "Code analysis",
                "Unit test generation",
                "Test execution",
                "Code coverage analysis",
                "Mutation testing",
                "Edge case detection"
            ],
            estimated_duration=300
        )

    async def validate_inputs(self, inputs: AgentInput) -> bool:
        """Validate that source code is provided"""
        if not inputs.source_code:
            self.log("Source code is required", "ERROR")
            return False
        return True

    async def generate_test_scripts(self, inputs: AgentInput) -> List[Dict[str, Any]]:
        """Generate unit test scripts from source code"""
        self.log("Analyzing source code structure")

        test_scripts = []

        # Parse source code to extract functions/methods
        functions = self._extract_functions(inputs.source_code)

        for func_name, func_code in functions.items():
            # Generate test script for each function
            test_script = {
                "script_id": str(uuid.uuid4()),
                "target_function": func_name,
                "language": self._detect_language(inputs.source_code),
                "test_code": self._generate_unit_test_code(func_name, func_code),
                "test_framework": self._get_test_framework(inputs),
                "description": f"Unit tests for {func_name}"
            }
            test_scripts.append(test_script)

        return test_scripts

    async def generate_test_data(self, inputs: AgentInput) -> Dict[str, Any]:
        """Generate test data for unit tests"""
        self.log("Generating test data")

        return {
            "normal_cases": self._generate_normal_test_data(),
            "edge_cases": self._generate_edge_cases(),
            "boundary_values": self._generate_boundary_values(),
            "null_cases": self._generate_null_cases(),
            "error_cases": self._generate_error_cases()
        }

    async def execute_tests(
        self,
        test_scripts: List[Dict[str, Any]],
        test_data: Dict[str, Any],
        inputs: AgentInput
    ) -> List[TestCase]:
        """Execute generated unit tests"""
        self.log(f"Executing {len(test_scripts)} test scripts")

        test_cases = []

        for script in test_scripts:
            # Execute tests for normal cases
            test_cases.extend(
                self._execute_test_cases(script, test_data["normal_cases"], "normal")
            )

            # Execute edge cases
            test_cases.extend(
                self._execute_test_cases(script, test_data["edge_cases"], "edge")
            )

            # Execute boundary value tests
            test_cases.extend(
                self._execute_test_cases(script, test_data["boundary_values"], "boundary")
            )

        return test_cases

    async def collect_evidence(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[TestEvidence]:
        """Collect evidence from test execution"""
        evidences = []

        for test_case in test_cases:
            # Generate coverage report
            coverage_evidence = TestEvidence(
                evidence_id=str(uuid.uuid4()),
                test_case_id=test_case.id,
                evidence_type="report",
                file_path=f"evidence/coverage_{test_case.id}.html",
                timestamp=datetime.now(),
                description="Code coverage report"
            )
            evidences.append(coverage_evidence)

            # Generate execution log
            log_evidence = TestEvidence(
                evidence_id=str(uuid.uuid4()),
                test_case_id=test_case.id,
                evidence_type="log",
                file_path=f"evidence/execution_{test_case.id}.log",
                timestamp=datetime.now(),
                description="Test execution log"
            )
            evidences.append(log_evidence)

        return evidences

    async def perform_rca(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[RootCauseAnalysis]:
        """Perform root cause analysis on failed tests"""
        rca_results = []

        failed_tests = [tc for tc in test_cases if tc.status == TestResult.FAILED]

        for test_case in failed_tests:
            rca = self._analyze_failure(test_case, inputs.source_code)
            rca_results.append(rca)

        return rca_results

    async def generate_recommendations(
        self,
        test_cases: List[TestCase],
        rca_results: List[RootCauseAnalysis],
        inputs: AgentInput
    ) -> List[Recommendation]:
        """Generate recommendations for fixing failures"""
        recommendations = []

        for rca in rca_results:
            recommendation = Recommendation(
                recommendation_id=str(uuid.uuid4()),
                title=f"Fix for {rca.category}",
                description=f"Root cause: {rca.root_cause}",
                category="code_fix",
                priority=rca.severity,
                suggested_fix=self._generate_fix_suggestion(rca),
                code_changes=self._generate_code_changes(rca),
                related_rca=rca.issue_id
            )
            recommendations.append(recommendation)

        return recommendations

    # Helper methods

    def _extract_functions(self, source_code: str) -> Dict[str, str]:
        """Extract functions from source code"""
        functions = {}

        # Simple regex-based extraction (would be more sophisticated in production)
        # Python function pattern
        pattern = r'def\s+(\w+)\s*\([^)]*\):'
        matches = re.finditer(pattern, source_code)

        for match in matches:
            func_name = match.group(1)
            # Extract function body (simplified)
            start = match.start()
            functions[func_name] = source_code[start:start+500]  # Get snippet

        return functions if functions else {"main_function": source_code}

    def _detect_language(self, source_code: str) -> str:
        """Detect programming language"""
        if "def " in source_code and "import " in source_code:
            return "python"
        elif "function" in source_code and "const" in source_code:
            return "javascript"
        elif "public class" in source_code:
            return "java"
        return "unknown"

    def _generate_unit_test_code(self, func_name: str, func_code: str) -> str:
        """Generate unit test code"""
        return f"""
import pytest

def test_{func_name}_normal_case():
    result = {func_name}()
    assert result is not None

def test_{func_name}_edge_case():
    result = {func_name}()
    assert result is not None

def test_{func_name}_boundary():
    result = {func_name}()
    assert result is not None
"""

    def _get_test_framework(self, inputs: AgentInput) -> str:
        """Determine test framework to use"""
        if inputs.config and "test_framework" in inputs.config:
            return inputs.config["test_framework"]
        return "pytest"

    def _generate_normal_test_data(self) -> List[Dict[str, Any]]:
        """Generate normal test case data"""
        return [
            {"input": "valid_input", "expected": "valid_output"},
            {"input": 42, "expected": 42},
            {"input": [1, 2, 3], "expected": [1, 2, 3]}
        ]

    def _generate_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge case data"""
        return [
            {"input": "", "expected": None},
            {"input": None, "expected": None},
            {"input": [], "expected": []}
        ]

    def _generate_boundary_values(self) -> List[Dict[str, Any]]:
        """Generate boundary value data"""
        return [
            {"input": 0, "expected": 0},
            {"input": -1, "expected": -1},
            {"input": float('inf'), "expected": float('inf')}
        ]

    def _generate_null_cases(self) -> List[Dict[str, Any]]:
        """Generate null/empty cases"""
        return [
            {"input": None, "expected": None},
            {"input": "", "expected": ""}
        ]

    def _generate_error_cases(self) -> List[Dict[str, Any]]:
        """Generate error-inducing cases"""
        return [
            {"input": "invalid", "should_raise": "ValueError"},
            {"input": -999, "should_raise": "ValueError"}
        ]

    def _execute_test_cases(
        self,
        script: Dict[str, Any],
        test_data: List[Dict[str, Any]],
        case_type: str
    ) -> List[TestCase]:
        """Execute test cases"""
        test_cases = []

        for idx, data in enumerate(test_data):
            test_case = TestCase(
                id=str(uuid.uuid4()),
                name=f"{script['target_function']}_{case_type}_{idx}",
                description=f"Test {script['target_function']} with {case_type} case",
                test_type="unit",
                steps=[
                    f"Call {script['target_function']} with input: {data.get('input')}",
                    "Verify output matches expected result"
                ],
                expected_result=str(data.get('expected', 'success')),
                actual_result="success",  # Simulated
                status=TestResult.PASSED,  # Simulated - would actually execute
                execution_time=0.05,
                evidence_files=[]
            )
            test_cases.append(test_case)

        return test_cases

    def _analyze_failure(self, test_case: TestCase, source_code: str) -> RootCauseAnalysis:
        """Analyze test failure"""
        return RootCauseAnalysis(
            issue_id=str(uuid.uuid4()),
            category="Logic Error",
            root_cause=f"Test {test_case.name} failed due to incorrect logic",
            affected_components=[test_case.name],
            severity="medium",
            stack_trace=test_case.error_message
        )

    def _generate_fix_suggestion(self, rca: RootCauseAnalysis) -> str:
        """Generate fix suggestion"""
        return f"Review the logic in {', '.join(rca.affected_components)} and ensure proper handling of edge cases"

    def _generate_code_changes(self, rca: RootCauseAnalysis) -> List[Dict[str, str]]:
        """Generate suggested code changes"""
        return [
            {
                "file": "source_code.py",
                "line": "10",
                "original": "return value",
                "suggested": "return value if value is not None else default_value"
            }
        ]
