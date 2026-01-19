# Azure AI Foundry Agent Extension

[![CI - Lint and Test](https://github.com/pablosalvador10/northwestern-msai-foundry-agent-extension/actions/workflows/ci.yml/badge.svg)](https://github.com/pablosalvador10/northwestern-msai-foundry-agent-extension/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Build AI agents with the Microsoft Agent Framework SDK and connect them to Azure Functions and Logic Apps as decoupled cloud-based tools. This project provides production-ready abstractions, comprehensive documentation, and step-by-step labs following Microsoft's official agent patterns.

## Built With Microsoft Agent Framework

This project uses the official Microsoft Agent Framework SDK (azure-ai-projects and azure-ai-agents) to create production-ready AI agents that can leverage Azure cloud services as tools.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Labs and Tutorials](#labs-and-tutorials)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [Resources](#resources)

## Features

- Microsoft Agent Framework: Built with official azure-ai-projects SDK
- Azure Functions Integration: Cloud-based computational tools
- Logic Apps Orchestration: Cloud-based workflow tools
- Decoupled Architecture: Tools deployed independently from agent
- Type Safety: Comprehensive type hints and Pydantic validation
- Production-Ready Logging: Structured logging with no print statements
- Security First: Managed Identity and Function Key authentication
- Async Support: Both synchronous and asynchronous APIs
- Comprehensive Tests: pytest-based test suite
- Step-by-Step Labs: Interactive Jupyter notebooks
- PEP8 Compliant: Black, Ruff, and MyPy enforced
- CI/CD Ready: GitHub Actions workflows

## Architecture

The system follows Microsoft Agent Framework patterns with decoupled cloud tools:

```
┌─────────────────────────────────────┐
│   Microsoft Agent Framework         │
│   (azure-ai-projects SDK)          │
│                                     │
│   ┌─────────────────────────────┐  │
│   │  AI Agent (GPT-4)           │  │
│   │  + Tool Registry            │  │
│   └───────────┬─────────────────┘  │
└───────────────┼─────────────────────┘
                │
         ┌──────┴──────┐
         │             │
    ┌────▼─────┐ ┌────▼──────┐
    │  Azure   │ │  Logic    │
    │ Function │ │   App     │
    │ (Cloud)  │ │ (Cloud)   │
    └──────────┘ └───────────┘
```

Key Principles:
- Agent in Isolation: Created using Microsoft Agent Framework
- Decoupled Tools: Azure Functions and Logic Apps deployed independently
- Tool Registration: Agent learns about cloud tools via registration
- Automatic Orchestration: Agent decides when to invoke tools
│  └──────────────┴──────────────┴─────────────────┘  │
└─────────────────────────────────────────────────────┘
```

For detailed architecture information, see:
- [Architecture Diagram and Overview](docs/architecture.md)
- [Design Rationale and Decisions](docs/rationale.md)

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or later
- Azure subscription
- **Azure AI Foundry project** (create at [ai.azure.com](https://ai.azure.com))
- Azure Functions deployed (optional for labs)
- Azure Logic Apps deployed (optional for labs)

### Installation

```bash
# Clone the repository
git clone https://github.com/pablosalvador10/northwestern-msai-foundry-agent-extension.git
cd northwestern-msai-foundry-agent-extension

# Install dependencies (includes azure-ai-projects SDK)
pip install -r requirements.txt
```

### Basic Usage with Microsoft Agent Framework

```python
from src.agent_core import AgentConfig, FoundryAgent
from src.abstractions.azure_functions import FunctionConfig
from src.abstractions.logic_apps import LogicAppConfig

# Step 1: Create an agent using Microsoft Agent Framework
agent_config = AgentConfig(
    project_endpoint="https://your-project.api.azureml.ms",  # Your AI Foundry project
    model_name="gpt-4",  # Your deployed model
    instructions="You are a helpful assistant with Azure tools."
)

agent = FoundryAgent(agent_config)

# Step 2: Register Azure Function as a tool (deployed in cloud)
function_config = FunctionConfig(
    function_url="https://your-app.azurewebsites.net/api/process",
    function_key="your-key"
)

agent.register_azure_function_tool(
    name="process_data",
    config=function_config,
    description="Processes numerical data and returns statistics"
)

# Step 3: Register Logic App as a tool (deployed in cloud)
logic_config = LogicAppConfig(
    workflow_url="https://prod-xx.logic.azure.com:443/workflows/..."
)

agent.register_logic_app_tool(
    name="send_notification",
    config=logic_config,
    description="Sends email notifications"
)

# Step 4: Create the agent with registered tools
agent_id = agent.create_agent(name="My Agent")

# Step 5: Run the agent - it will automatically use tools as needed
response = agent.run_agent(
    agent_id,
    "Process these numbers: 10, 20, 30, 40, 50 and email the results"
)
print(response)
```

## 📁 Project Structure

```
northwestern-msai-foundry-agent-extension/
├── src/                          # Source code
│   ├── abstractions/             # Azure service abstractions
│   │   ├── azure_functions.py    # Azure Functions client
│   │   └── logic_apps.py         # Logic Apps client
│   ├── agent_core.py             # AI Foundry agent core
│   └── __init__.py
├── tests/                        # Test suite
│   ├── test_azure_functions.py   # Functions tests
│   ├── test_logic_apps.py        # Logic Apps tests
│   ├── conftest.py               # Test fixtures
│   └── __init__.py
├── notebooks/                    # Interactive labs
│   ├── lab1_azure_functions.ipynb
│   ├── lab2_logic_apps.ipynb
│   └── lab3_complete_agent.ipynb
├── docs/                         # Documentation
│   ├── architecture.md           # Architecture diagram & overview
│   └── rationale.md              # Design decisions
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project configuration
└── README.md                     # This file
```

## 💻 Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Development Installation

```bash
# Install with development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## 📖 Usage Examples

### Azure Functions

```python
from src.abstractions.azure_functions import (
    FunctionConfig,
    DataProcessorFunction,
    IntegrationFunction
)

# Data Processing
config = FunctionConfig(
    function_url="https://app.azurewebsites.net/api/process",
    function_key="key123"
)
processor = DataProcessorFunction(config)
result = processor.process_data({"values": [1, 2, 3]})

# External Integration
integration = IntegrationFunction(config)
result = integration.call_external_service(
    service="weather-api",
    params={"location": "Chicago"}
)
```

### Logic Apps

```python
from src.abstractions.logic_apps import (
    LogicAppConfig,
    WorkflowOrchestrator,
    NotificationWorkflow
)

# Workflow Orchestration
config = LogicAppConfig(
    workflow_url="https://prod-123.eastus.logic.azure.com:443/workflows/...",
    timeout=60
)
orchestrator = WorkflowOrchestrator(config)
result = orchestrator.execute_workflow(
    workflow_type="approval",
    data={"amount": 5000}
)

# Notifications
notifier = NotificationWorkflow(config)
result = notifier.send_notification(
    recipient="admin@company.com",
    subject="Alert",
    message="System alert detected"
)
```

### Full Agent Integration

```python
from src.agent_core import AgentConfig, FoundryAgent

# Configure agent
agent = FoundryAgent(AgentConfig(
    endpoint="https://your-endpoint.openai.azure.com",
    api_key="your-api-key"
))

# Register tools
agent.register_azure_function("processor", function_config)
agent.register_logic_app("notifier", logic_app_config)

# Run agent
response = agent.run("Process data and send notification")
```

## 🧪 Labs and Tutorials

Interactive Jupyter notebooks provide hands-on learning:

1. **[Lab 1: Azure Functions Integration](notebooks/lab1_azure_functions.ipynb)**
   - Configure Azure Functions client
   - Synchronous and asynchronous invocation
   - Error handling and best practices

2. **[Lab 2: Logic Apps Integration](notebooks/lab2_logic_apps.ipynb)**
   - Trigger Logic App workflows
   - Workflow orchestration
   - Notification workflows

3. **[Lab 3: Complete Agent Integration](notebooks/lab3_complete_agent.ipynb)**
   - Build a full AI Foundry agent
   - Register multiple tools
   - Multi-tool workflow orchestration

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Azure Functions
AZURE_FUNCTION_URL=https://your-app.azurewebsites.net/api/function
AZURE_FUNCTION_KEY=your-function-key

# Logic Apps
LOGIC_APP_URL=https://prod-123.eastus.logic.azure.com:443/workflows/...
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=your-resource-group

# Azure OpenAI / AI Foundry
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_MODEL=gpt-4

# Optional: Managed Identity (production)
AZURE_CLIENT_ID=your-client-id
AZURE_TENANT_ID=your-tenant-id
```

### Authentication Options

**Development**: Use Function Keys and API Keys
```python
config = FunctionConfig(
    function_url="...",
    function_key="your-key"
)
```

**Production**: Use Managed Identity
```python
config = FunctionConfig(
    function_url="...",
    use_managed_identity=True
)
```

## 🧪 Testing

### Run All Tests

```bash
# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_azure_functions.py -v

# Run with markers
pytest tests/ -v -m unit
```

### Linting and Type Checking

```bash
# Ruff linting
ruff check src/ tests/

# Black formatting
black --check src/ tests/

# MyPy type checking
mypy src/ --ignore-missing-imports
```

### Run All Quality Checks

```bash
# Run linting
ruff check src/ tests/

# Run formatting check
black --check src/ tests/

# Run type checking
mypy src/

# Run tests
pytest tests/ -v --cov=src
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow PEP8 and use type hints
4. Add tests for new functionality
5. Ensure all tests pass and coverage remains high
6. Use structured logging (no print statements)
7. Update documentation as needed
8. Submit a pull request

### Code Quality Standards

- **PEP8 Compliance**: Use Black for formatting
- **Type Hints**: All functions must have type annotations
- **Docstrings**: Follow PEP 257 conventions
- **Logging**: Use logging module, no print statements
- **Error Handling**: Comprehensive try-except with logging
- **Tests**: Maintain 90%+ code coverage

## 🤖 GitHub Copilot Tips

### In VS Code

Enable GitHub Copilot and use these prompts in comments:

```python
# Create an Azure Function that processes JSON data and returns statistics
# Add retry logic with exponential backoff to this function call
# Generate unit tests for the AzureFunctionsClient class
# Add error handling for network timeouts and HTTP errors
```

### In Copilot Chat

Use these commands:
- `/explain` - Understand Azure service integration code
- `/fix` - Fix errors in function calls or configurations
- `/tests` - Generate comprehensive tests
- `/doc` - Generate docstrings and documentation

### Useful Prompts

- "Create a new Azure Function tool for sentiment analysis"
- "Add monitoring and metrics to the agent core"
- "Implement circuit breaker pattern for Azure service calls"
- "Generate a Logic App workflow for customer onboarding"

## 🔗 Resources

### Azure Portal & UI

- [Azure Portal](https://portal.azure.com) - Main Azure portal
- [Azure AI Foundry Studio](https://ai.azure.com) - AI Studio interface
- [Azure Functions](https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.Web%2Fsites/kind/functionapp) - Function Apps management
- [Logic Apps](https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.Logic%2Fworkflows) - Logic Apps designer
- [Application Insights](https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/microsoft.insights%2Fcomponents) - Monitoring and diagnostics

### Documentation

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-studio/)
- [Azure Functions Documentation](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Azure Logic Apps Documentation](https://learn.microsoft.com/en-us/azure/logic-apps/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure Identity (Managed Identity)](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/)

### Python Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)
- [Pytest Documentation](https://docs.pytest.org/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Northwestern University MSAI Program
- Azure AI Foundry Team
- Contributors and maintainers

---

**Built with ❤️ for the Northwestern MSAI community**
