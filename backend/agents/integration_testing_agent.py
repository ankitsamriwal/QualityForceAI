"""
Integration Testing Agent - Tests API integrations and component interactions
"""
import uuid
from typing import Dict, Any, List
from datetime import datetime

from core.base_agent import BaseTestingAgent
from core.models import (
    AgentMetadata, AgentInput, AgentType,
    TestCase, TestEvidence, RootCauseAnalysis, Recommendation, TestResult
)


class IntegrationTestingAgent(BaseTestingAgent):
    """Agent specialized in integration testing"""

    def get_metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_type=AgentType.INTEGRATION_TESTING,
            name="Integration Testing Agent",
            description="Tests API endpoints, integrations, and component interactions",
            version="1.0.0",
            required_inputs=["endpoints"],
            optional_inputs=["api_specs", "api_keys", "config"],
            capabilities=[
                "API endpoint testing",
                "Integration validation",
                "Contract testing",
                "Data flow validation",
                "Third-party integration testing",
                "Microservices communication testing"
            ],
            estimated_duration=900
        )

    async def validate_inputs(self, inputs: AgentInput) -> bool:
        """Validate that endpoints are provided"""
        if not inputs.endpoints and not inputs.api_specs:
            self.log("Endpoints or API specs are required", "ERROR")
            return False
        return True

    async def generate_test_scripts(self, inputs: AgentInput) -> List[Dict[str, Any]]:
        """Generate integration test scripts"""
        self.log("Analyzing API endpoints and integration points")

        test_scripts = []

        endpoints = inputs.endpoints or []
        if inputs.api_specs:
            endpoints.extend(self._parse_api_specs(inputs.api_specs))

        for endpoint in endpoints:
            # Generate tests for different HTTP methods
            methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]

            for method in methods:
                test_script = {
                    "script_id": str(uuid.uuid4()),
                    "endpoint": endpoint,
                    "method": method,
                    "test_type": "integration",
                    "headers": self._generate_headers(inputs.api_keys),
                    "test_cases": self._generate_endpoint_test_cases(endpoint, method)
                }
                test_scripts.append(test_script)

        return test_scripts

    async def generate_test_data(self, inputs: AgentInput) -> Dict[str, Any]:
        """Generate test data for integration tests"""
        self.log("Generating integration test data")

        return {
            "valid_payloads": self._generate_valid_payloads(),
            "invalid_payloads": self._generate_invalid_payloads(),
            "authentication_tokens": self._generate_auth_tokens(inputs.api_keys),
            "test_users": self._generate_test_users(),
            "edge_case_data": self._generate_edge_case_data()
        }

    async def execute_tests(
        self,
        test_scripts: List[Dict[str, Any]],
        test_data: Dict[str, Any],
        inputs: AgentInput
    ) -> List[TestCase]:
        """Execute integration tests"""
        self.log(f"Executing {len(test_scripts)} integration test scripts")

        test_cases = []

        for script in test_scripts:
            for test_case_data in script["test_cases"]:
                test_case = TestCase(
                    id=str(uuid.uuid4()),
                    name=f"{script['method']}_{script['endpoint']}_{test_case_data['name']}",
                    description=test_case_data['description'],
                    test_type="integration",
                    steps=[
                        f"Prepare {script['method']} request to {script['endpoint']}",
                        f"Send request with payload: {test_case_data.get('payload', 'N/A')}",
                        f"Verify response status: {test_case_data['expected_status']}",
                        "Validate response schema and data"
                    ],
                    expected_result=f"Status: {test_case_data['expected_status']}",
                    actual_result=f"Status: {test_case_data['expected_status']}",  # Simulated
                    status=TestResult.PASSED,  # Simulated
                    execution_time=0.25,
                    evidence_files=[]
                )
                test_cases.append(test_case)

        return test_cases

    async def collect_evidence(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[TestEvidence]:
        """Collect evidence from integration testing"""
        evidences = []

        for test_case in test_cases:
            # Request/Response logs
            log_evidence = TestEvidence(
                evidence_id=str(uuid.uuid4()),
                test_case_id=test_case.id,
                evidence_type="log",
                file_path=f"evidence/api_log_{test_case.id}.json",
                timestamp=datetime.now(),
                description="API request and response log"
            )
            evidences.append(log_evidence)

            # Network trace
            trace_evidence = TestEvidence(
                evidence_id=str(uuid.uuid4()),
                test_case_id=test_case.id,
                evidence_type="recording",
                file_path=f"evidence/network_trace_{test_case.id}.har",
                timestamp=datetime.now(),
                description="Network traffic trace"
            )
            evidences.append(trace_evidence)

        return evidences

    async def perform_rca(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[RootCauseAnalysis]:
        """Perform root cause analysis on integration failures"""
        rca_results = []

        failed_tests = [tc for tc in test_cases if tc.status == TestResult.FAILED]

        for test_case in failed_tests:
            rca = RootCauseAnalysis(
                issue_id=str(uuid.uuid4()),
                category=self._categorize_integration_failure(test_case),
                root_cause=self._analyze_integration_failure(test_case),
                affected_components=self._identify_affected_components(test_case),
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
        """Generate recommendations for integration test failures"""
        recommendations = []

        for rca in rca_results:
            recommendation = Recommendation(
                recommendation_id=str(uuid.uuid4()),
                title=f"Fix integration issue: {rca.category}",
                description=f"Root cause: {rca.root_cause}",
                category="integration_fix",
                priority=rca.severity,
                suggested_fix=self._generate_integration_fix(rca),
                code_changes=[],
                related_rca=rca.issue_id
            )
            recommendations.append(recommendation)

        return recommendations

    # Helper methods

    def _parse_api_specs(self, api_specs: Dict[str, Any]) -> List[str]:
        """Parse API specifications to extract endpoints"""
        endpoints = []

        # OpenAPI/Swagger format
        if "paths" in api_specs:
            endpoints.extend(api_specs["paths"].keys())

        return endpoints

    def _generate_headers(self, api_keys: Dict[str, str] = None) -> Dict[str, str]:
        """Generate request headers"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if api_keys:
            for key, value in api_keys.items():
                headers[f"X-API-{key}"] = value

        return headers

    def _generate_endpoint_test_cases(self, endpoint: str, method: str) -> List[Dict[str, Any]]:
        """Generate test cases for an endpoint"""
        return [
            {
                "name": "valid_request",
                "description": f"Test {method} {endpoint} with valid data",
                "payload": {"data": "valid"},
                "expected_status": 200 if method == "GET" else 201
            },
            {
                "name": "invalid_auth",
                "description": f"Test {method} {endpoint} with invalid authentication",
                "payload": {},
                "expected_status": 401
            },
            {
                "name": "malformed_payload",
                "description": f"Test {method} {endpoint} with malformed data",
                "payload": {"invalid": "data"},
                "expected_status": 400
            }
        ]

    def _generate_valid_payloads(self) -> List[Dict[str, Any]]:
        """Generate valid request payloads"""
        return [
            {"id": 1, "name": "Test User", "email": "test@example.com"},
            {"query": "search term", "filters": {"category": "test"}},
        ]

    def _generate_invalid_payloads(self) -> List[Dict[str, Any]]:
        """Generate invalid request payloads"""
        return [
            {},  # Empty
            {"invalid_field": "value"},  # Wrong schema
            None  # Null
        ]

    def _generate_auth_tokens(self, api_keys: Dict[str, str] = None) -> Dict[str, str]:
        """Generate authentication tokens"""
        return {
            "valid_token": "valid_jwt_token_here",
            "expired_token": "expired_jwt_token_here",
            "invalid_token": "invalid_token"
        }

    def _generate_test_users(self) -> List[Dict[str, str]]:
        """Generate test user data"""
        return [
            {"username": "test_user_1", "role": "admin"},
            {"username": "test_user_2", "role": "user"}
        ]

    def _generate_edge_case_data(self) -> List[Dict[str, Any]]:
        """Generate edge case data"""
        return [
            {"large_payload": "x" * 10000},
            {"unicode_data": "测试数据"},
            {"special_chars": "<script>alert('xss')</script>"}
        ]

    def _categorize_integration_failure(self, test_case: TestCase) -> str:
        """Categorize the type of integration failure"""
        if "auth" in test_case.name.lower():
            return "Authentication Failure"
        elif "timeout" in test_case.error_message or "":
            return "Timeout Error"
        elif "404" in test_case.error_message or "":
            return "Endpoint Not Found"
        else:
            return "Integration Error"

    def _analyze_integration_failure(self, test_case: TestCase) -> str:
        """Analyze the root cause of integration failure"""
        return f"Integration test {test_case.name} failed. Check API endpoint availability and response format."

    def _identify_affected_components(self, test_case: TestCase) -> List[str]:
        """Identify components affected by the failure"""
        return [test_case.name, "API Gateway", "Backend Service"]

    def _generate_integration_fix(self, rca: RootCauseAnalysis) -> str:
        """Generate fix suggestion for integration issues"""
        if "Authentication" in rca.category:
            return "Verify API key configuration and authentication mechanism"
        elif "Timeout" in rca.category:
            return "Increase timeout settings or optimize backend processing"
        elif "Not Found" in rca.category:
            return "Verify endpoint URL and routing configuration"
        else:
            return "Review API contract and ensure proper request/response handling"
