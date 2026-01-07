# QualityForce AI - User Guide

## Introduction

QualityForce AI is an intelligent testing automation platform that provides specialized AI agents for comprehensive software testing. This guide will help you get started and make the most of the platform.

## Getting Started

### 1. Accessing the Platform

Open your browser and navigate to `http://localhost:5173` (frontend) after starting both backend and frontend servers.

### 2. Dashboard Overview

The Dashboard provides a high-level overview of your testing operations:
- Total executions count
- Active executions
- Test results summary
- Pass/fail rates
- Recent execution history

## Using Testing Agents

### Available Agents

#### Unit Testing Agent
**Purpose:** Generate and execute unit tests for source code

**Required Inputs:**
- Source code

**Use Cases:**
- Testing individual functions and methods
- Code coverage analysis
- Edge case detection
- Mutation testing

**Example:**
```python
# Input your Python function
def calculate_total(items):
    return sum(item['price'] for item in items)
```

The agent will generate comprehensive unit tests including:
- Normal case tests
- Edge cases (empty list, None values)
- Boundary value tests

#### Functional Testing Agent
**Purpose:** Validate functionality against requirements

**Required Inputs:**
- Requirements document, FRD, or BRD

**Use Cases:**
- Acceptance testing
- User story validation
- Feature completeness verification
- Workflow testing

**Example:**
```
Requirements:
- System must allow users to register with email and password
- Password must be at least 8 characters
- Email verification required
```

#### Integration Testing Agent
**Purpose:** Test API endpoints and integrations

**Required Inputs:**
- API endpoints

**Optional Inputs:**
- API specifications (OpenAPI/Swagger)
- API keys/credentials

**Use Cases:**
- API contract testing
- Service integration validation
- End-to-end workflow testing
- Third-party integration testing

**Example:**
```
Endpoints:
- /api/users (GET, POST)
- /api/products (GET, POST, PUT, DELETE)
```

#### Security Testing / VAPT Agent
**Purpose:** Comprehensive security testing and vulnerability assessment

**Required Inputs:**
- API endpoints OR source code

**Use Cases:**
- OWASP Top 10 testing
- SQL injection detection
- XSS vulnerability scanning
- Authentication/authorization testing
- Security misconfiguration detection

**Example:**
The agent will automatically test for:
- Injection attacks
- Broken authentication
- Sensitive data exposure
- Security misconfigurations

#### Load Testing Agent
**Purpose:** Test system performance under expected load

**Required Inputs:**
- API endpoints

**Use Cases:**
- Performance baseline establishment
- Capacity planning
- SLA validation
- Response time measurement

**Example:**
```
Configuration:
- Normal load: 100 concurrent users
- Peak load: 500 concurrent users
- Duration: 10 minutes
```

#### Stress Testing Agent
**Purpose:** Test system behavior under extreme conditions

**Required Inputs:**
- API endpoints

**Use Cases:**
- Breaking point identification
- System stability testing
- Recovery testing
- Scalability assessment

#### Regression Testing Agent
**Purpose:** Ensure existing functionality remains intact

**Required Inputs:**
- Source code OR endpoints

**Use Cases:**
- Post-deployment validation
- Change impact analysis
- Continuous integration testing
- Version comparison

## Step-by-Step Workflow

### 1. Select Agents

1. Navigate to the **Marketplace** page
2. Browse available agents
3. Click on an agent card to select it
4. Selected agents are highlighted with a blue border

### 2. Configure Inputs

1. Click **"Configure Inputs"** on selected agents
2. Fill in required inputs:
   - Source code (for unit/regression testing)
   - Requirements documents (for functional testing)
   - API endpoints (for integration/security/performance testing)
   - API keys (if testing secured endpoints)

### 3. Execute Tests

1. Click the **"Execute"** button in the top-right
2. The system will start all selected agents
3. For multiple agents, they run concurrently by default

### 4. Monitor Execution

1. Navigate to the **Executions** page
2. View real-time status of running tests
3. Active executions show a spinner and progress
4. You can cancel running executions if needed

### 5. View Results

1. Click **"View"** icon on any execution
2. Or navigate to **Results** page and select an execution

#### Results Page Sections:

**Summary Statistics:**
- Total tests executed
- Pass/fail counts
- Pass rate percentage
- Execution duration

**Test Cases:**
- Detailed list of all test cases
- Status (passed/failed/skipped)
- Execution time
- Error messages for failures

**Root Cause Analysis:**
- Identified issues
- Root cause description
- Affected components
- Severity level

**Recommendations:**
- AI-generated fix suggestions
- Specific code changes
- Priority levels
- Implementation guidance

## Best Practices

### 1. Input Quality

**For Source Code:**
- Provide complete, compilable code
- Include imports and dependencies
- Use meaningful variable/function names

**For Requirements:**
- Be specific and measurable
- Include acceptance criteria
- Define expected behavior clearly

**For API Testing:**
- Provide complete endpoint URLs
- Include authentication details
- Specify expected response formats

### 2. Agent Selection

**Use Multiple Agents:**
- Combine unit + integration testing for full coverage
- Add security testing for public-facing APIs
- Include performance testing for high-traffic systems

**Sequential vs Parallel:**
- Use parallel execution for independent tests
- Use sequential for dependent tests

### 3. Interpreting Results

**Focus on Failures:**
- Review failed tests first
- Check RCA for root causes
- Apply recommendations systematically

**Monitor Trends:**
- Track pass rates over time
- Identify flaky tests
- Monitor performance metrics

### 4. Acting on Recommendations

1. **Review Priority:**
   - Critical/High: Address immediately
   - Medium: Plan for next sprint
   - Low: Include in backlog

2. **Validate Fixes:**
   - Apply suggested code changes
   - Re-run tests to verify
   - Update test baselines

3. **Continuous Improvement:**
   - Learn from RCA patterns
   - Update requirements based on findings
   - Refine test inputs

## Advanced Features

### Batch Execution

Execute multiple agents with different configurations:

```python
# Via API
{
  "executions": [
    {
      "agent_type": "unit_testing",
      "inputs": {"source_code": "..."}
    },
    {
      "agent_type": "security_testing",
      "inputs": {"endpoints": ["..."]}
    }
  ],
  "parallel": true
}
```

### Custom Configuration

Customize agent behavior:

```json
{
  "config": {
    "test_framework": "pytest",
    "coverage_threshold": 80,
    "max_tests": 100,
    "timeout": 600
  }
}
```

### Evidence Collection

All executions collect evidence:
- Execution logs
- Coverage reports
- Screenshots (for UI tests)
- Network traces
- Performance metrics

Access via Results page or API.

## Troubleshooting

### Agent Not Starting

- Check required inputs are provided
- Verify backend is running
- Check browser console for errors

### Tests Failing Unexpectedly

- Review RCA for root causes
- Check input data quality
- Verify environment setup

### Performance Issues

- Reduce concurrent executions
- Increase execution timeout
- Check system resources

### No Results Showing

- Wait for execution to complete
- Check execution status
- Refresh the page

## FAQ

**Q: Can I run multiple agents simultaneously?**
A: Yes, select multiple agents and they'll run concurrently.

**Q: How long are results stored?**
A: Results are stored indefinitely until manually deleted.

**Q: Can I export results?**
A: Yes, via the API or use browser's save/print feature.

**Q: What if my API requires authentication?**
A: Provide API keys in the agent inputs configuration.

**Q: Can I integrate this with CI/CD?**
A: Yes, use the REST API to trigger executions programmatically.

## Support

For issues or questions:
- Check the API Documentation
- Review example usage in README
- Submit an issue on GitHub
