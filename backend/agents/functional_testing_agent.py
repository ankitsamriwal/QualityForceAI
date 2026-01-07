"""
Functional Testing Agent - Tests functional requirements
"""
import uuid
from typing import Dict, Any, List
from datetime import datetime

from core.base_agent import BaseTestingAgent
from core.models import (
    AgentMetadata, AgentInput, AgentType,
    TestCase, TestEvidence, RootCauseAnalysis, Recommendation, TestResult
)


class FunctionalTestingAgent(BaseTestingAgent):
    """Agent specialized in functional testing based on requirements"""

    def get_metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_type=AgentType.FUNCTIONAL_TESTING,
            name="Functional Testing Agent",
            description="Validates application functionality against requirements (FRD/BRD)",
            version="1.0.0",
            required_inputs=["requirements_doc"],
            optional_inputs=["frd", "brd", "config"],
            capabilities=[
                "Requirements analysis",
                "Test scenario generation",
                "User story validation",
                "Acceptance criteria testing",
                "Workflow validation",
                "Feature completeness testing"
            ],
            estimated_duration=600
        )

    async def validate_inputs(self, inputs: AgentInput) -> bool:
        """Validate that requirements are provided"""
        if not inputs.requirements_doc and not inputs.frd and not inputs.brd:
            self.log("At least one requirements document is required", "ERROR")
            return False
        return True

    async def generate_test_scripts(self, inputs: AgentInput) -> List[Dict[str, Any]]:
        """Generate functional test scripts from requirements"""
        self.log("Parsing requirements documents")

        test_scripts = []

        # Parse requirements
        requirements = self._parse_requirements(inputs)

        for req_id, requirement in requirements.items():
            test_script = {
                "script_id": str(uuid.uuid4()),
                "requirement_id": req_id,
                "requirement_text": requirement["text"],
                "test_scenario": self._create_test_scenario(requirement),
                "acceptance_criteria": requirement.get("acceptance_criteria", []),
                "test_type": "functional",
                "priority": requirement.get("priority", "medium")
            }
            test_scripts.append(test_script)

        return test_scripts

    async def generate_test_data(self, inputs: AgentInput) -> Dict[str, Any]:
        """Generate test data for functional tests"""
        self.log("Generating functional test data")

        return {
            "user_personas": self._generate_user_personas(),
            "test_scenarios": self._generate_test_scenarios(),
            "workflow_data": self._generate_workflow_data(),
            "input_variations": self._generate_input_variations()
        }

    async def execute_tests(
        self,
        test_scripts: List[Dict[str, Any]],
        test_data: Dict[str, Any],
        inputs: AgentInput
    ) -> List[TestCase]:
        """Execute functional tests"""
        self.log(f"Executing {len(test_scripts)} functional test scripts")

        test_cases = []

        for script in test_scripts:
            # Create test cases for each acceptance criterion
            for idx, criterion in enumerate(script.get("acceptance_criteria", ["default"])):
                test_case = TestCase(
                    id=str(uuid.uuid4()),
                    name=f"{script['requirement_id']}_AC{idx+1}",
                    description=f"Validate: {criterion}",
                    test_type="functional",
                    steps=self._generate_test_steps(script, criterion),
                    expected_result=criterion,
                    actual_result="Requirement met",  # Simulated
                    status=TestResult.PASSED,  # Simulated
                    execution_time=1.5,
                    evidence_files=[]
                )
                test_cases.append(test_case)

        return test_cases

    async def collect_evidence(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[TestEvidence]:
        """Collect evidence from functional testing"""
        evidences = []

        for test_case in test_cases:
            # Screenshot evidence
            screenshot = TestEvidence(
                evidence_id=str(uuid.uuid4()),
                test_case_id=test_case.id,
                evidence_type="screenshot",
                file_path=f"evidence/screenshot_{test_case.id}.png",
                timestamp=datetime.now(),
                description="UI state after test execution"
            )
            evidences.append(screenshot)

            # Test report
            report = TestEvidence(
                evidence_id=str(uuid.uuid4()),
                test_case_id=test_case.id,
                evidence_type="report",
                file_path=f"evidence/functional_report_{test_case.id}.pdf",
                timestamp=datetime.now(),
                description="Detailed functional test report"
            )
            evidences.append(report)

        return evidences

    async def perform_rca(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[RootCauseAnalysis]:
        """Perform root cause analysis on failed functional tests"""
        rca_results = []

        failed_tests = [tc for tc in test_cases if tc.status == TestResult.FAILED]

        for test_case in failed_tests:
            rca = RootCauseAnalysis(
                issue_id=str(uuid.uuid4()),
                category="Functional Requirement Not Met",
                root_cause=f"The implementation does not satisfy the acceptance criteria: {test_case.expected_result}",
                affected_components=[test_case.name],
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
        """Generate recommendations for functional test failures"""
        recommendations = []

        for rca in rca_results:
            recommendation = Recommendation(
                recommendation_id=str(uuid.uuid4()),
                title=f"Implement missing functionality",
                description=f"Root cause: {rca.root_cause}",
                category="feature_implementation",
                priority=rca.severity,
                suggested_fix="Review the requirement specification and implement the missing functionality",
                code_changes=[],
                related_rca=rca.issue_id
            )
            recommendations.append(recommendation)

        return recommendations

    # Helper methods

    def _parse_requirements(self, inputs: AgentInput) -> Dict[str, Dict[str, Any]]:
        """Parse requirements from documents"""
        requirements = {}

        # Parse from different document types
        if inputs.requirements_doc:
            requirements.update(self._extract_requirements(inputs.requirements_doc))

        if inputs.frd:
            requirements.update(self._extract_requirements(inputs.frd, "functional"))

        if inputs.brd:
            requirements.update(self._extract_requirements(inputs.brd, "business"))

        return requirements

    def _extract_requirements(self, doc: str, doc_type: str = "general") -> Dict[str, Dict[str, Any]]:
        """Extract individual requirements from document"""
        requirements = {}

        # Simple parsing (would use NLP in production)
        lines = doc.split('\n')
        req_counter = 1

        for line in lines:
            if line.strip().startswith(('REQ', 'FR', 'BR', '-', '*')):
                req_id = f"{doc_type.upper()}-{req_counter:03d}"
                requirements[req_id] = {
                    "text": line.strip(),
                    "type": doc_type,
                    "priority": "high",
                    "acceptance_criteria": [
                        f"System must {line.strip().lower()}",
                        "User can verify the functionality"
                    ]
                }
                req_counter += 1

        # If no structured requirements found, create a default one
        if not requirements:
            requirements["REQ-001"] = {
                "text": "System functionality validation",
                "type": doc_type,
                "priority": "medium",
                "acceptance_criteria": ["System works as expected"]
            }

        return requirements

    def _create_test_scenario(self, requirement: Dict[str, Any]) -> str:
        """Create test scenario from requirement"""
        return f"""
Scenario: Validate {requirement['text']}
Given: The system is in a ready state
When: User performs the required action
Then: {requirement['text']} is satisfied
"""

    def _generate_user_personas(self) -> List[Dict[str, str]]:
        """Generate user personas for testing"""
        return [
            {"name": "Admin User", "role": "administrator", "permissions": "full"},
            {"name": "Regular User", "role": "user", "permissions": "standard"},
            {"name": "Guest User", "role": "guest", "permissions": "limited"}
        ]

    def _generate_test_scenarios(self) -> List[Dict[str, Any]]:
        """Generate test scenarios"""
        return [
            {
                "scenario": "Happy Path",
                "description": "User completes workflow successfully"
            },
            {
                "scenario": "Alternative Path",
                "description": "User takes alternative route"
            },
            {
                "scenario": "Error Path",
                "description": "System handles errors gracefully"
            }
        ]

    def _generate_workflow_data(self) -> Dict[str, Any]:
        """Generate workflow test data"""
        return {
            "workflows": [
                "User registration",
                "User login",
                "Data submission",
                "Report generation"
            ]
        }

    def _generate_input_variations(self) -> List[Dict[str, Any]]:
        """Generate input variations for testing"""
        return [
            {"type": "valid", "value": "valid_input"},
            {"type": "invalid", "value": "invalid@input"},
            {"type": "edge_case", "value": ""}
        ]

    def _generate_test_steps(self, script: Dict[str, Any], criterion: str) -> List[str]:
        """Generate detailed test steps"""
        return [
            "Navigate to the feature under test",
            "Enter required test data",
            "Execute the functionality",
            f"Verify that: {criterion}",
            "Document the results"
        ]
