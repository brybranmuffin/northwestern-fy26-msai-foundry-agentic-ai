# Laboratory Notebooks

## Overview

These notebooks provide step-by-step tutorials for building AI agents with Azure Functions and Logic Apps using the **Microsoft Agent Framework SDK**.

## Notebooks

### Lab 1: Azure Functions Integration
**File**: `lab1_azure_functions.ipynb`

Learn how to:
- Deploy Azure Functions as cloud-based tools
- Configure function endpoints and authentication
- Test functions independently

### Lab 2: Logic Apps Integration  
**File**: `lab2_logic_apps.ipynb`

Learn how to:
- Deploy Logic App workflows  
- Configure workflow triggers
- Test workflows independently

### Lab 3: Complete Agent with Microsoft Agent Framework
**File**: `lab3_complete_agent.ipynb`

**The complete end-to-end story:**

1. **Create an Agent in Isolation**
   - Using `azure-ai-projects` SDK
   - Configure Azure AI Foundry project
   - Create agent with instructions

2. **Deploy Tools in the Cloud**
   - Azure Functions for computation
   - Logic Apps for workflows
   - Keep tools decoupled from agent

3. **Register Tools with Agent**
   - Register Azure Functions as tools
   - Register Logic Apps as tools
   - Agent learns tool capabilities

4. **Run Agent with Tools**
   - Agent decides when to use tools
   - Automatic tool invocation
   - Response synthesis

## Prerequisites

- Azure subscription
- Azure AI Foundry project
- Python 3.10+
- Dependencies installed (`pip install -r requirements.txt`)

## Getting Started

1. Complete setup in Lab 1 and Lab 2
2. Deploy your Azure Functions and Logic Apps
3. Configure environment variables in `.env`
4. Follow Lab 3 for complete integration

## Microsoft Agent Framework

These labs use the official **Microsoft Agent Framework SDK**:
- `azure-ai-projects` - For project and agent management
- `azure-ai-agents` - For agent operations

### Key Concepts

**Decoupled Architecture**:
- Agent code separate from tool implementation
- Tools deployed independently in Azure
- Scale and update independently

**Tool Registration**:
```python
agent.register_azure_function_tool(
    name="process_data",
    config=function_config,  # Points to cloud function
    description="Processes numerical data"
)
```

**Agent Orchestration**:
- Agent analyzes user requests
- Decides which tools to use
- Invokes cloud services automatically
- Synthesizes responses

## Resources

- [Microsoft Agent Framework Docs](https://learn.microsoft.com/en-us/agent-framework/)
- [Azure AI Foundry](https://ai.azure.com)
- [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Logic Apps](https://learn.microsoft.com/en-us/azure/logic-apps/)
