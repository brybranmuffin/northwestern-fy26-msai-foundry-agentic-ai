# Quick Start Guide

This guide will get you up and running with the Azure AI Foundry Agent Extension in under 10 minutes.

## Prerequisites

- Python 3.10 or later
- Azure subscription (for deploying functions/logic apps)
- pip package manager

## Step 1: Clone and Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/pablosalvador10/northwestern-msai-foundry-agent-extension.git
cd northwestern-msai-foundry-agent-extension

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure Environment (3 minutes)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Azure credentials
# At minimum, set:
# - AZURE_FUNCTION_URL
# - AZURE_FUNCTION_KEY
# - LOGIC_APP_URL
```

## Step 3: Run Your First Example (2 minutes)

### Azure Function Example

```python
from src.abstractions.azure_functions import FunctionConfig, AzureFunctionsClient

# Configure
config = FunctionConfig(
    function_url="https://your-app.azurewebsites.net/api/function",
    function_key="your-key"
)

# Use
client = AzureFunctionsClient(config)
result = client.invoke_function({"data": "test"})
print(result)
```

### Logic App Example

```python
from src.abstractions.logic_apps import LogicAppConfig, LogicAppsClient

# Configure
config = LogicAppConfig(
    workflow_url="https://prod-123.eastus.logic.azure.com:443/workflows/..."
)

# Use
client = LogicAppsClient(config)
result = client.trigger_workflow({"action": "test"})
print(result)
```

## Step 4: Explore Interactive Labs (3 minutes)

Open Jupyter notebooks for hands-on learning:

```bash
# Install Jupyter if needed
pip install jupyter

# Launch notebooks
jupyter notebook notebooks/
```

Start with:
1. `lab1_azure_functions.ipynb` - Learn Azure Functions integration
2. `lab2_logic_apps.ipynb` - Learn Logic Apps orchestration
3. `lab3_complete_agent.ipynb` - Build a complete AI agent

## Step 5: Run Tests (Optional)

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src
```

## Common Use Cases

### Use Case 1: Data Processing

```python
from src.abstractions.azure_functions import DataProcessorFunction, FunctionConfig

config = FunctionConfig(
    function_url="https://your-app.azurewebsites.net/api/process",
    function_key="your-key"
)

processor = DataProcessorFunction(config)
result = processor.process_data({"values": [1, 2, 3, 4, 5]})
```

### Use Case 2: Workflow Orchestration

```python
from src.abstractions.logic_apps import WorkflowOrchestrator, LogicAppConfig

config = LogicAppConfig(
    workflow_url="https://prod-123.eastus.logic.azure.com:443/workflows/..."
)

orchestrator = WorkflowOrchestrator(config)
result = orchestrator.execute_workflow(
    workflow_type="approval",
    data={"amount": 5000, "requester": "user@company.com"}
)
```

### Use Case 3: AI Agent with Tools

```python
from src.agent_core import AgentConfig, FoundryAgent
from src.abstractions.azure_functions import FunctionConfig
from src.abstractions.logic_apps import LogicAppConfig

# Configure agent
agent = FoundryAgent(AgentConfig(
    endpoint="https://your-endpoint.openai.azure.com",
    api_key="your-api-key"
))

# Register tools
agent.register_azure_function("processor", function_config)
agent.register_logic_app("notifier", logic_app_config)

# Use the agent
response = agent.run("Process these numbers: 1, 2, 3, 4, 5")
print(response)
```

## Troubleshooting

### Issue: Module Not Found

```bash
# Make sure you're in the project directory
cd northwestern-msai-foundry-agent-extension

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Azure Authentication Failed

- Verify your function keys and endpoint URLs in `.env`
- Check that your Azure resources are deployed and accessible
- Try using a simple HTTP client (curl/Postman) to test endpoints directly

### Issue: Tests Failing

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run tests with verbose output
pytest tests/ -v -s
```

## Next Steps

1. **Deploy Your Own Azure Resources**
   - [Create an Azure Function App](https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal)
   - [Create a Logic App](https://learn.microsoft.com/en-us/azure/logic-apps/quickstart-create-example-consumption-workflow)

2. **Customize the Agent**
   - Add your own tools in `src/abstractions/`
   - Extend the agent core in `src/agent_core.py`

3. **Build Your Application**
   - Use the abstractions as building blocks
   - Create custom workflows for your use case

4. **Contribute**
   - Found a bug? Open an issue
   - Have an improvement? Submit a PR

## Resources

- [Full Documentation](README.md)
- [Architecture Overview](docs/architecture.md)
- [Design Rationale](docs/rationale.md)
- [Azure Portal](https://portal.azure.com)
- [Azure AI Foundry](https://ai.azure.com)

## Support

- 📧 Issues: [GitHub Issues](https://github.com/pablosalvador10/northwestern-msai-foundry-agent-extension/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/pablosalvador10/northwestern-msai-foundry-agent-extension/discussions)
- 📚 Documentation: [docs/](docs/)

---

**Happy coding! 🚀**
