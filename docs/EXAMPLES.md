# QualityForce AI - Examples

This document provides practical examples of using the QualityForce AI Testing Agent Marketplace.

## Table of Contents

1. [Unit Testing Examples](#unit-testing-examples)
2. [Functional Testing Examples](#functional-testing-examples)
3. [Integration Testing Examples](#integration-testing-examples)
4. [Security Testing Examples](#security-testing-examples)
5. [Performance Testing Examples](#performance-testing-examples)
6. [Batch Execution Examples](#batch-execution-examples)

## Unit Testing Examples

### Example 1: Testing a Python Calculator

```python
import requests

source_code = """
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
"""

response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "unit_testing",
    "inputs": {
        "source_code": source_code,
        "libraries": ["pytest"]
    }
})

print(f"Execution ID: {response.json()['execution_id']}")
```

### Example 2: Testing JavaScript Functions

```javascript
// Via UI or API
const sourceCode = `
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function sanitizeInput(input) {
    return input.replace(/[<>]/g, '');
}
`;

// Submit via marketplace UI
```

## Functional Testing Examples

### Example 1: E-commerce Requirements Testing

```python
requirements_doc = """
User Story: Shopping Cart Management

As a customer,
I want to manage items in my shopping cart,
So that I can purchase products.

Acceptance Criteria:
- User can add items to cart
- User can remove items from cart
- User can update item quantities
- Cart total is calculated correctly
- Cart persists across sessions
- Out-of-stock items cannot be added
"""

response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "functional_testing",
    "inputs": {
        "requirements_doc": requirements_doc
    }
})
```

### Example 2: Banking Application FRD

```python
frd = """
Functional Requirements Document: Money Transfer

FR-001: User Authentication
- System shall authenticate users before allowing transfers
- Multi-factor authentication required for transfers > $1000

FR-002: Transfer Validation
- System shall validate recipient account exists
- System shall verify sufficient balance
- System shall enforce daily transfer limits

FR-003: Transaction Processing
- System shall process transfers in real-time
- System shall generate unique transaction IDs
- System shall send confirmation emails
"""

response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "functional_testing",
    "inputs": {
        "frd": frd
    }
})
```

## Integration Testing Examples

### Example 1: REST API Testing

```python
response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "integration_testing",
    "inputs": {
        "endpoints": [
            "https://api.example.com/v1/users",
            "https://api.example.com/v1/products",
            "https://api.example.com/v1/orders"
        ],
        "api_keys": {
            "Authorization": "Bearer YOUR_API_TOKEN",
            "X-API-Key": "your-api-key"
        }
    }
})
```

### Example 2: OpenAPI Spec Testing

```python
import json

openapi_spec = {
    "openapi": "3.0.0",
    "info": {"title": "My API", "version": "1.0.0"},
    "paths": {
        "/users": {
            "get": {"summary": "List users"},
            "post": {"summary": "Create user"}
        },
        "/users/{id}": {
            "get": {"summary": "Get user"},
            "put": {"summary": "Update user"},
            "delete": {"summary": "Delete user"}
        }
    }
}

response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "integration_testing",
    "inputs": {
        "api_specs": openapi_spec,
        "endpoints": ["https://api.example.com"]
    }
})
```

## Security Testing Examples

### Example 1: Web Application Security Scan

```python
response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "security_testing",
    "inputs": {
        "endpoints": [
            "https://myapp.com/login",
            "https://myapp.com/api/users",
            "https://myapp.com/api/products"
        ]
    }
})
```

### Example 2: Source Code Security Analysis

```python
vulnerable_code = """
def login(username, password):
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    # Hardcoded credentials
    admin_password = "admin123"

    # XSS vulnerability
    return f"<div>Welcome {username}</div>"
"""

response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "security_testing",
    "inputs": {
        "source_code": vulnerable_code
    }
})
```

## Performance Testing Examples

### Example 1: Load Testing

```python
response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "load_testing",
    "inputs": {
        "endpoints": ["https://api.example.com/products"],
        "config": {
            "concurrent_users": 100,
            "duration": 300,  # 5 minutes
            "ramp_up_time": 30
        }
    }
})
```

### Example 2: Stress Testing

```python
response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "stress_testing",
    "inputs": {
        "endpoints": ["https://api.example.com/orders"],
        "config": {
            "max_users": 5000,
            "duration": 600,
            "ramp_up_time": 60
        }
    }
})
```

## Batch Execution Examples

### Example 1: Complete Test Suite

```python
# Execute full test suite for a new feature
response = requests.post('http://localhost:8000/api/executions/execute/batch', json={
    "executions": [
        {
            "agent_type": "unit_testing",
            "inputs": {
                "source_code": "... your code ..."
            }
        },
        {
            "agent_type": "functional_testing",
            "inputs": {
                "requirements_doc": "... your requirements ..."
            }
        },
        {
            "agent_type": "integration_testing",
            "inputs": {
                "endpoints": ["/api/new-feature"]
            }
        },
        {
            "agent_type": "security_testing",
            "inputs": {
                "endpoints": ["/api/new-feature"]
            }
        }
    ],
    "parallel": True,
    "continue_on_failure": True
})

print(f"Batch execution started: {response.json()}")
```

### Example 2: Pre-Deployment Testing

```python
# Comprehensive testing before production deployment
response = requests.post('http://localhost:8000/api/executions/execute/batch', json={
    "executions": [
        {
            "agent_type": "regression_testing",
            "inputs": {
                "source_code": "... entire codebase ..."
            }
        },
        {
            "agent_type": "integration_testing",
            "inputs": {
                "endpoints": ["... all endpoints ..."]
            }
        },
        {
            "agent_type": "security_testing",
            "inputs": {
                "endpoints": ["... all endpoints ..."]
            }
        },
        {
            "agent_type": "load_testing",
            "inputs": {
                "endpoints": ["... critical endpoints ..."]
            }
        }
    ],
    "parallel": True,
    "continue_on_failure": False  # Stop on first failure
})
```

### Example 3: Monitoring Results

```python
import time

# Start batch execution
batch_response = requests.post('http://localhost:8000/api/executions/execute/batch', json={
    "executions": [...],
    "parallel": True
})

execution_ids = batch_response.json()['executions'].values()

# Monitor progress
while True:
    all_complete = True

    for exec_id in execution_ids:
        status_response = requests.get(
            f'http://localhost:8000/api/executions/{exec_id}/status'
        )
        status = status_response.json()['status']

        print(f"Execution {exec_id}: {status}")

        if status in ['pending', 'running']:
            all_complete = False

    if all_complete:
        break

    time.sleep(5)

# Collect all results
for exec_id in execution_ids:
    result = requests.get(f'http://localhost:8000/api/results/{exec_id}')
    print(f"\nResults for {exec_id}:")
    print(f"Total tests: {result.json()['total_tests']}")
    print(f"Passed: {result.json()['passed_tests']}")
    print(f"Failed: {result.json()['failed_tests']}")
```

## Working with Results

### Example 1: Analyzing Test Results

```python
execution_id = "your-execution-id"

# Get summary
summary = requests.get(f'http://localhost:8000/api/results/{execution_id}/summary')
print("Summary:", summary.json())

# Get failed tests
test_cases = requests.get(f'http://localhost:8000/api/results/{execution_id}/test-cases')
failed_tests = [
    tc for tc in test_cases.json()['test_cases']
    if tc['status'] == 'failed'
]

print(f"\nFailed tests: {len(failed_tests)}")
for test in failed_tests:
    print(f"- {test['name']}: {test.get('error_message', 'No error message')}")
```

### Example 2: Implementing Recommendations

```python
# Get recommendations
recs = requests.get(f'http://localhost:8000/api/results/{execution_id}/recommendations')

for rec in recs.json()['recommendations']:
    print(f"\n{rec['title']} (Priority: {rec['priority']})")
    print(f"Fix: {rec['suggested_fix']}")

    if rec.get('code_changes'):
        for change in rec['code_changes']:
            print(f"\nFile: {change['file']}, Line: {change['line']}")
            print(f"Original: {change['original']}")
            print(f"Suggested: {change['suggested']}")
```

## CI/CD Integration

### Example: GitHub Actions

```yaml
name: QualityForce AI Testing

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run QualityForce AI Tests
        run: |
          python scripts/run_tests.py
```

```python
# scripts/run_tests.py
import requests
import sys

# Read source code
with open('src/main.py') as f:
    source_code = f.read()

# Execute tests
response = requests.post('http://qualityforce-ai:8000/api/executions/execute/batch', json={
    "executions": [
        {"agent_type": "unit_testing", "inputs": {"source_code": source_code}},
        {"agent_type": "security_testing", "inputs": {"source_code": source_code}}
    ],
    "parallel": True
})

# Wait and check results
# ... (implementation)

# Exit with error code if tests failed
if failed_tests > 0:
    sys.exit(1)
```

## Conclusion

These examples demonstrate the flexibility and power of the QualityForce AI Testing Agent Marketplace. Combine different agents, customize inputs, and integrate with your development workflow for comprehensive automated testing.
