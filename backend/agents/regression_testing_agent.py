"""
Regression Testing Agent - Ensures existing functionality remains intact
"""
import uuid
from typing import Dict, Any, List
from datetime import datetime

from core.base_agent import BaseTestingAgent
from core.models import (
    AgentMetadata, AgentInput, AgentType,
    TestCase, TestEvidence, RootCauseAnalysis, Recommendation, TestResult
)


class RegressionTestingAgent(BaseTestingAgent):
    """Agent specialized in regression testing"""

    def get_metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_type=AgentType.REGRESSION_TESTING,
            name="Regression Testing Agent",
            description="Validates that existing functionality works after changes",
            version="1.0.0",
            required_inputs=["source_code"],
            optional_inputs=["requirements_doc", "endpoints", "config"],
            capabilities=[
                "Baseline test suite execution",
                "Change impact analysis",
                "Test prioritization",
                "Visual regression testing",
                "API regression testing",
                "Performance regression detection"
            ],
            estimated_duration=900
        )

    async def validate_inputs(self, inputs: AgentInput) -> bool:
        """Validate inputs for regression testing"""
        if not inputs.source_code and not inputs.endpoints:
            self.log("Source code or endpoints required for regression testing", "ERROR")
            return False
        return True

    async def generate_test_scripts(self, inputs: AgentInput) -> List[Dict[str, Any]]:
        """Generate regression test scripts"""
        self.log("Generating regression test suite")

        test_scripts = []

        # Categories of regression tests
        regression_categories = [
            "critical_path",
            "high_risk_areas",
            "previously_failed",
            "boundary_cases",
            "integration_points"
        ]

        for category in regression_categories:
            test_script = {
                "script_id": str(uuid.uuid4()),
                "category": category,
                "test_type": "regression",
                "priority": self._get_category_priority(category),
                "test_suite": self._get_test_suite_for_category(category)
            }
            test_scripts.append(test_script)

        return test_scripts

    async def generate_test_data(self, inputs: AgentInput) -> Dict[str, Any]:
        """Generate test data for regression testing"""
        self.log("Generating regression test data")

        return {
            "baseline_results": self._load_baseline_results(),
            "test_data": self._generate_regression_test_data(),
            "comparison_snapshots": self._generate_snapshots(),
            "historical_data": self._load_historical_data()
        }

    async def execute_tests(
        self,
        test_scripts: List[Dict[str, Any]],
        test_data: Dict[str, Any],
        inputs: AgentInput
    ) -> List[TestCase]:
        """Execute regression tests"""
        self.log(f"Executing {len(test_scripts)} regression test suites")

        test_cases = []

        for script in test_scripts:
            for test_suite_item in script["test_suite"]:
                test_case = TestCase(
                    id=str(uuid.uuid4()),
                    name=f"Regression_{script['category']}_{test_suite_item['name']}",
                    description=f"Regression test: {test_suite_item['description']}",
                    test_type="regression",
                    steps=test_suite_item["steps"],
                    expected_result=test_suite_item["expected_result"],
                    actual_result=test_suite_item["expected_result"],  # Simulated
                    status=TestResult.PASSED,  # Simulated
                    execution_time=0.8,
                    evidence_files=[]
                )
                test_cases.append(test_case)

        # Compare with baseline
        self._compare_with_baseline(test_cases, test_data["baseline_results"])

        return test_cases

    async def collect_evidence(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[TestEvidence]:
        """Collect regression test evidence"""
        evidences = []

        for test_case in test_cases:
            # Comparison report
            comparison = TestEvidence(
                evidence_id=str(uuid.uuid4()),
                test_case_id=test_case.id,
                evidence_type="report",
                file_path=f"evidence/regression_comparison_{test_case.id}.html",
                timestamp=datetime.now(),
                description="Baseline vs current comparison"
            )
            evidences.append(comparison)

            # Visual diff (for UI tests)
            if "ui" in test_case.name.lower():
                visual_diff = TestEvidence(
                    evidence_id=str(uuid.uuid4()),
                    test_case_id=test_case.id,
                    evidence_type="screenshot",
                    file_path=f"evidence/visual_diff_{test_case.id}.png",
                    timestamp=datetime.now(),
                    description="Visual regression comparison"
                )
                evidences.append(visual_diff)

        return evidences

    async def perform_rca(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[RootCauseAnalysis]:
        """Analyze regression failures"""
        rca_results = []

        failed_tests = [tc for tc in test_cases if tc.status == TestResult.FAILED]

        for test_case in failed_tests:
            rca = RootCauseAnalysis(
                issue_id=str(uuid.uuid4()),
                category="Regression Detected",
                root_cause=self._analyze_regression(test_case),
                affected_components=self._identify_changed_components(test_case),
                severity="high",
                stack_trace=test_case.error_message
            )
            rca_results.append(rca)

        return rca_results

    async def generate_recommendations(
        self,
        test_cases: List[TestCase],
        rca_results: List[RootCauseAnalysis],
        inputs: AgentInput
    ) -> List[Recommendation]:
        """Generate recommendations for regression fixes"""
        recommendations = []

        for rca in rca_results:
            recommendation = Recommendation(
                recommendation_id=str(uuid.uuid4()),
                title=f"Fix Regression: {rca.category}",
                description=f"Root cause: {rca.root_cause}",
                category="regression_fix",
                priority=rca.severity,
                suggested_fix=self._generate_regression_fix(rca),
                code_changes=self._identify_problematic_changes(rca),
                related_rca=rca.issue_id
            )
            recommendations.append(recommendation)

        return recommendations

    # Helper methods

    def _get_category_priority(self, category: str) -> str:
        """Get priority level for test category"""
        priority_map = {
            "critical_path": "critical",
            "high_risk_areas": "high",
            "previously_failed": "high",
            "boundary_cases": "medium",
            "integration_points": "medium"
        }
        return priority_map.get(category, "low")

    def _get_test_suite_for_category(self, category: str) -> List[Dict[str, Any]]:
        """Get test suite for a category"""
        return [
            {
                "name": f"{category}_test_1",
                "description": f"Test existing functionality for {category}",
                "steps": [
                    "Execute baseline test",
                    "Compare with previous results",
                    "Verify no regression"
                ],
                "expected_result": "Behavior matches baseline"
            },
            {
                "name": f"{category}_test_2",
                "description": f"Validate integration for {category}",
                "steps": [
                    "Test component interactions",
                    "Verify data flow",
                    "Check error handling"
                ],
                "expected_result": "All integrations work correctly"
            }
        ]

    def _load_baseline_results(self) -> Dict[str, Any]:
        """Load baseline test results"""
        return {
            "version": "1.0.0",
            "timestamp": "2024-01-01T00:00:00",
            "results": {}
        }

    def _generate_regression_test_data(self) -> Dict[str, Any]:
        """Generate test data for regression tests"""
        return {
            "test_inputs": ["input1", "input2", "input3"],
            "expected_outputs": ["output1", "output2", "output3"]
        }

    def _generate_snapshots(self) -> List[str]:
        """Generate UI/data snapshots for comparison"""
        return ["snapshot_1.json", "snapshot_2.json"]

    def _load_historical_data(self) -> Dict[str, Any]:
        """Load historical test data"""
        return {
            "test_runs": 100,
            "average_pass_rate": 0.95,
            "flaky_tests": []
        }

    def _compare_with_baseline(
        self,
        test_cases: List[TestCase],
        baseline: Dict[str, Any]
    ):
        """Compare current results with baseline"""
        # Implementation would compare test results with baseline
        # and mark tests as failed if there's a regression
        pass

    def _analyze_regression(self, test_case: TestCase) -> str:
        """Analyze what caused the regression"""
        return f"Test {test_case.name} behavior changed from baseline. Review recent code changes."

    def _identify_changed_components(self, test_case: TestCase) -> List[str]:
        """Identify which components changed"""
        return [
            test_case.name,
            "Related Module",
            "Dependent Component"
        ]

    def _generate_regression_fix(self, rca: RootCauseAnalysis) -> str:
        """Generate fix for regression"""
        return f"Review changes in {', '.join(rca.affected_components)} and restore expected behavior"

    def _identify_problematic_changes(self, rca: RootCauseAnalysis) -> List[Dict[str, str]]:
        """Identify problematic code changes"""
        return [
            {
                "file": "component.py",
                "line": "42",
                "original": "return process_data(input)",
                "suggested": "# Review this change - may have introduced regression"
            }
        ]
