# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Agents API

### List All Agents

```http
GET /agents/
```

Returns list of all available testing agents with their metadata.

**Response:**
```json
[
  {
    "agent_type": "unit_testing",
    "name": "Unit Testing Agent",
    "description": "Generates and executes comprehensive unit tests for source code",
    "version": "1.0.0",
    "required_inputs": ["source_code"],
    "optional_inputs": ["libraries", "config"],
    "capabilities": [
      "Code analysis",
      "Unit test generation",
      "Test execution",
      "Code coverage analysis"
    ],
    "estimated_duration": 300
  }
]
```

### Get Agent Details

```http
GET /agents/{agent_type}
```

Returns detailed metadata for a specific agent.

**Parameters:**
- `agent_type` (path) - Type of agent (e.g., "unit_testing", "security_testing")

## Executions API

### Execute Single Agent

```http
POST /executions/execute
```

Execute a single testing agent.

**Request Body:**
```json
{
  "agent_type": "unit_testing",
  "inputs": {
    "source_code": "def add(a, b): return a + b",
    "libraries": ["pytest"],
    "config": {}
  },
  "config": {
    "test_framework": "pytest"
  }
}
```

**Response:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "message": "Agent unit_testing execution started"
}
```

### Execute Multiple Agents (Batch)

```http
POST /executions/execute/batch
```

Execute multiple agents concurrently or sequentially.

**Request Body:**
```json
{
  "executions": [
    {
      "agent_type": "unit_testing",
      "inputs": {
        "source_code": "..."
      }
    },
    {
      "agent_type": "integration_testing",
      "inputs": {
        "endpoints": ["/api/users"]
      }
    }
  ],
  "parallel": true,
  "continue_on_failure": true
}
```

**Response:**
```json
{
  "executions": {
    "unit_testing": "exec-id-1",
    "integration_testing": "exec-id-2"
  },
  "status": "started",
  "parallel": true,
  "total_agents": 2
}
```

### Get Execution Status

```http
GET /executions/{execution_id}/status
```

Get current status of an execution.

**Response:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running"
}
```

Status values: `pending`, `running`, `completed`, `failed`, `cancelled`

### Get Execution Result

```http
GET /executions/{execution_id}/result
```

Get complete execution result.

**Response:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_type": "unit_testing",
  "status": "completed",
  "start_time": "2024-01-01T10:00:00",
  "end_time": "2024-01-01T10:05:00",
  "duration": 300.0,
  "total_tests": 15,
  "passed_tests": 12,
  "failed_tests": 3,
  "skipped_tests": 0,
  "error_tests": 0,
  "test_cases": [...],
  "root_cause_analyses": [...],
  "recommendations": [...],
  "logs": [...],
  "metrics": {}
}
```

### Cancel Execution

```http
POST /executions/{execution_id}/cancel
```

Cancel a running execution.

**Response:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "cancelled"
}
```

### List All Executions

```http
GET /executions/
```

Get list of all executions.

### Get Active Execution Count

```http
GET /executions/active/count
```

**Response:**
```json
{
  "active_executions": 3
}
```

## Results API

### Get Result

```http
GET /results/{execution_id}
```

Get execution result by ID.

### Get Test Cases

```http
GET /results/{execution_id}/test-cases
```

Get all test cases for an execution.

**Response:**
```json
{
  "execution_id": "...",
  "total_tests": 15,
  "passed": 12,
  "failed": 3,
  "skipped": 0,
  "errors": 0,
  "test_cases": [
    {
      "id": "test-1",
      "name": "test_add_positive_numbers",
      "description": "Test addition with positive numbers",
      "test_type": "unit",
      "steps": [...],
      "expected_result": "...",
      "actual_result": "...",
      "status": "passed",
      "execution_time": 0.05
    }
  ]
}
```

### Get Root Cause Analysis

```http
GET /results/{execution_id}/rca
```

Get RCA results for failed tests.

**Response:**
```json
{
  "execution_id": "...",
  "total_issues": 2,
  "rca_results": [
    {
      "issue_id": "rca-1",
      "category": "Logic Error",
      "root_cause": "Incorrect validation logic for negative numbers",
      "affected_components": ["calculate_discount"],
      "severity": "high",
      "stack_trace": "..."
    }
  ]
}
```

### Get Recommendations

```http
GET /results/{execution_id}/recommendations
```

Get AI-generated fix recommendations.

**Response:**
```json
{
  "execution_id": "...",
  "total_recommendations": 2,
  "recommendations": [
    {
      "recommendation_id": "rec-1",
      "title": "Fix input validation",
      "description": "Add proper validation for negative numbers",
      "category": "code_fix",
      "priority": "high",
      "suggested_fix": "Add validation check: if value < 0: raise ValueError(...)",
      "code_changes": [
        {
          "file": "discount.py",
          "line": "5",
          "original": "return price * discount",
          "suggested": "if discount < 0:\n    raise ValueError('Invalid discount')\nreturn price * discount"
        }
      ],
      "related_rca": "rca-1"
    }
  ]
}
```

### Get Execution Summary

```http
GET /results/{execution_id}/summary
```

Get summarized execution results.

### Delete Result

```http
DELETE /results/{execution_id}
```

Delete execution result and associated evidence.

### List All Results

```http
GET /results/
```

Get list of all stored execution IDs.

### Get Storage Statistics

```http
GET /results/stats/storage
```

**Response:**
```json
{
  "total_executions": 50,
  "results_size_bytes": 1048576,
  "evidence_size_bytes": 2097152,
  "total_size_mb": 3.0
}
```

## Input Schemas

### Agent Input

```typescript
{
  source_code?: string          // Source code to test
  requirements_doc?: string     // Requirements document
  frd?: string                  // Functional Requirements Document
  brd?: string                  // Business Requirements Document
  libraries?: string[]          // List of libraries/dependencies
  endpoints?: string[]          // API endpoints to test
  api_specs?: object            // OpenAPI/Swagger specs
  api_keys?: object             // API keys and credentials
  architecture_doc?: string     // Architecture documentation
  config?: object               // Additional configuration
}
```

### Configuration Options

```typescript
{
  test_framework?: string       // e.g., "pytest", "jest"
  timeout?: number              // Execution timeout in seconds
  max_tests?: number           // Maximum tests to generate
  coverage_threshold?: number  // Minimum coverage percentage
}
```

## Error Responses

All endpoints return standard error responses:

```json
{
  "detail": "Error message description"
}
```

**Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error
