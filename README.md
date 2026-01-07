# QualityForce AI - Testing Agent Marketplace

<div align="center">

**AI-Powered Testing Automation Platform**

A comprehensive testing agent marketplace that provides specialized AI agents for various testing needs including unit testing, functional testing, integration testing, security testing, performance testing, and regression testing.

</div>

## Features

### Multiple Specialized Testing Agents

- **Unit Testing Agent** - Generates and executes comprehensive unit tests for source code
- **Functional Testing Agent** - Validates application functionality against requirements (FRD/BRD)
- **Integration Testing Agent** - Tests API endpoints, integrations, and component interactions
- **Security Testing / VAPT Agent** - Performs comprehensive security testing and vulnerability assessment
- **Load Testing Agent** - Tests system performance under expected load conditions
- **Stress Testing Agent** - Tests system behavior under extreme load conditions
- **Regression Testing Agent** - Validates that existing functionality remains intact after changes

### Intelligent Testing Capabilities

Each agent provides:
- **Automated Test Script Generation** - AI-powered test case generation based on inputs
- **Test Data Generation** - Smart test data creation for various scenarios
- **Execution with Evidence** - Complete test execution with detailed evidence collection
- **Root Cause Analysis (RCA)** - Automated failure analysis to identify root causes
- **Auto Recommendations** - AI-generated fix suggestions based on failures
- **Concurrent Execution** - Run multiple agents simultaneously for faster results

### Comprehensive Inputs Support

- Source code, libraries, and dependencies
- Requirements documents (FRD, BRD, functional, architecture)
- API endpoints, specifications, and credentials
- Configuration files and environment settings

### Rich Results & Evidence

- Detailed test results with pass/fail status
- Execution logs and traces
- Screenshots and recordings
- Coverage reports
- RCA with severity classification
- Code-level fix recommendations

## Architecture

```
QualityForceAI/
├── backend/                 # Python FastAPI backend
│   ├── agents/             # Testing agent implementations
│   ├── api/                # REST API endpoints
│   ├── core/               # Core framework & marketplace
│   └── main.py             # Application entry point
├── frontend/               # React TypeScript frontend
│   └── src/
│       ├── components/     # UI components
│       ├── pages/          # Application pages
│       └── lib/            # API client & utilities
└── docs/                   # Documentation
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Create .env file
cp ../.env.example .env

# Run the backend
python main.py
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

### 1. Browse Agent Marketplace

Navigate to the Marketplace page to see all available testing agents with their capabilities and requirements.

### 2. Configure and Execute Agents

- Select one or more agents
- Provide required inputs (source code, requirements, endpoints, etc.)
- Click "Execute" to start testing

### 3. Monitor Execution

Track real-time execution status in the Execution Monitor page:
- View active executions
- Monitor progress
- Cancel running tests if needed

### 4. Review Results

View comprehensive test results including:
- Test case details with pass/fail status
- Root cause analysis for failures
- AI-generated recommendations for fixes
- Evidence files (logs, screenshots, reports)

## API Documentation

### Agent Endpoints

**GET /api/agents/** - List all available agents
```json
[
  {
    "agent_type": "unit_testing",
    "name": "Unit Testing Agent",
    "description": "Generates and executes comprehensive unit tests",
    "required_inputs": ["source_code"],
    "capabilities": ["Code analysis", "Unit test generation", ...]
  }
]
```

**POST /api/executions/execute** - Execute a single agent
```json
{
  "agent_type": "unit_testing",
  "inputs": {
    "source_code": "def add(a, b): return a + b",
    "libraries": ["pytest"]
  }
}
```

**POST /api/executions/execute/batch** - Execute multiple agents
```json
{
  "executions": [
    {"agent_type": "unit_testing", "inputs": {...}},
    {"agent_type": "integration_testing", "inputs": {...}}
  ],
  "parallel": true
}
```

**GET /api/executions/{execution_id}/result** - Get execution results
```json
{
  "execution_id": "123",
  "agent_type": "unit_testing",
  "status": "completed",
  "total_tests": 10,
  "passed_tests": 8,
  "failed_tests": 2,
  "test_cases": [...],
  "root_cause_analyses": [...],
  "recommendations": [...]
}
```

### Results Endpoints

- **GET /api/results/{execution_id}** - Get full results
- **GET /api/results/{execution_id}/test-cases** - Get test cases
- **GET /api/results/{execution_id}/rca** - Get RCA results
- **GET /api/results/{execution_id}/recommendations** - Get recommendations

## Example Usage

### Unit Testing Example

```python
import requests

# Execute unit testing agent
response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "unit_testing",
    "inputs": {
        "source_code": """
        def calculate_discount(price, discount_percent):
            if discount_percent < 0 or discount_percent > 100:
                raise ValueError("Invalid discount percentage")
            return price * (1 - discount_percent / 100)
        """
    }
})

execution_id = response.json()['execution_id']

# Get results
results = requests.get(f'http://localhost:8000/api/results/{execution_id}')
print(results.json())
```

### Integration Testing Example

```python
# Execute integration testing agent
response = requests.post('http://localhost:8000/api/executions/execute', json={
    "agent_type": "integration_testing",
    "inputs": {
        "endpoints": [
            "/api/users",
            "/api/products",
            "/api/orders"
        ],
        "api_keys": {
            "Authorization": "Bearer token123"
        }
    }
})
```

### Batch Execution Example

```python
# Execute multiple agents concurrently
response = requests.post('http://localhost:8000/api/executions/execute/batch', json={
    "executions": [
        {
            "agent_type": "unit_testing",
            "inputs": {"source_code": "..."}
        },
        {
            "agent_type": "security_testing",
            "inputs": {"endpoints": ["..."]}
        },
        {
            "agent_type": "load_testing",
            "inputs": {"endpoints": ["..."]}
        }
    ],
    "parallel": True
})
```

## Development

### Project Structure

- **Backend (`backend/`)** - FastAPI application with testing agents
  - `agents/` - Individual agent implementations
  - `core/` - Base agent framework, marketplace, storage
  - `api/` - REST API routes

- **Frontend (`frontend/`)** - React TypeScript application
  - `pages/` - Main application pages
  - `components/` - Reusable UI components
  - `lib/` - API client and utilities

### Adding a New Agent

1. Create agent class in `backend/agents/`:
```python
from core.base_agent import BaseTestingAgent

class MyNewAgent(BaseTestingAgent):
    def get_metadata(self):
        # Return agent metadata
        pass

    async def generate_test_scripts(self, inputs):
        # Generate test scripts
        pass

    # Implement other required methods...
```

2. Register agent in `backend/core/marketplace.py`:
```python
self.agents[AgentType.MY_NEW_AGENT] = MyNewAgent
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions, please visit the GitHub repository.
