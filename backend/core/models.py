"""
Core data models and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class AgentType(str, Enum):
    """Types of testing agents available"""
    UNIT_TESTING = "unit_testing"
    CODE_REVIEW = "code_review"
    BLACKBOX_TESTING = "blackbox_testing"
    BOUNDARY_VALUE_ANALYSIS = "boundary_value_analysis"
    TEST_VALIDATION = "test_validation"
    FUNCTIONAL_TESTING = "functional_testing"
    INTEGRATION_TESTING = "integration_testing"
    REGRESSION_TESTING = "regression_testing"
    SECURITY_TESTING = "security_testing"
    VAPT = "vapt"
    LOAD_TESTING = "load_testing"
    STRESS_TESTING = "stress_testing"


class ExecutionStatus(str, Enum):
    """Execution status states"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TestResult(str, Enum):
    """Individual test result status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class AgentInput(BaseModel):
    """Input configuration for an agent"""
    source_code: Optional[str] = None
    requirements_doc: Optional[str] = None
    frd: Optional[str] = None  # Functional Requirements Document
    brd: Optional[str] = None  # Business Requirements Document
    libraries: Optional[List[str]] = None
    endpoints: Optional[List[str]] = None
    api_specs: Optional[Dict[str, Any]] = None
    api_keys: Optional[Dict[str, str]] = None
    architecture_doc: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class AgentMetadata(BaseModel):
    """Agent metadata and capabilities"""
    agent_type: AgentType
    name: str
    description: str
    version: str = "1.0.0"
    required_inputs: List[str]
    optional_inputs: List[str]
    capabilities: List[str]
    estimated_duration: Optional[int] = None  # in seconds


class TestCase(BaseModel):
    """Individual test case"""
    id: str
    name: str
    description: str
    test_type: str
    steps: List[str]
    expected_result: str
    actual_result: Optional[str] = None
    status: Optional[TestResult] = None
    execution_time: Optional[float] = None
    error_message: Optional[str] = None
    evidence_files: List[str] = Field(default_factory=list)


class RootCauseAnalysis(BaseModel):
    """Root cause analysis for failures"""
    issue_id: str
    category: str
    root_cause: str
    affected_components: List[str]
    severity: Literal["low", "medium", "high", "critical"]
    stack_trace: Optional[str] = None


class Recommendation(BaseModel):
    """Auto-generated recommendation"""
    recommendation_id: str
    title: str
    description: str
    category: str
    priority: Literal["low", "medium", "high", "critical"]
    suggested_fix: str
    code_changes: Optional[List[Dict[str, str]]] = None
    related_rca: Optional[str] = None


class TestEvidence(BaseModel):
    """Test execution evidence"""
    evidence_id: str
    test_case_id: str
    evidence_type: Literal["screenshot", "log", "recording", "report", "data"]
    file_path: str
    timestamp: datetime
    description: Optional[str] = None


class AgentExecutionResult(BaseModel):
    """Result from agent execution"""
    execution_id: str
    agent_type: AgentType
    status: ExecutionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None

    # Generated outputs
    test_scripts: List[Dict[str, Any]] = Field(default_factory=list)
    test_data: Optional[Dict[str, Any]] = None
    test_cases: List[TestCase] = Field(default_factory=list)
    evidences: List[TestEvidence] = Field(default_factory=list)

    # Analysis
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    error_tests: int = 0

    # RCA and Recommendations
    root_cause_analyses: List[RootCauseAnalysis] = Field(default_factory=list)
    recommendations: List[Recommendation] = Field(default_factory=list)

    # Metadata
    logs: List[str] = Field(default_factory=list)
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)


class ExecutionRequest(BaseModel):
    """Request to execute an agent"""
    agent_type: AgentType
    inputs: AgentInput
    config: Optional[Dict[str, Any]] = None


class BatchExecutionRequest(BaseModel):
    """Request to execute multiple agents concurrently"""
    executions: List[ExecutionRequest]
    parallel: bool = True
    continue_on_failure: bool = True
