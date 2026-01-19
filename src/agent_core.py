"""
Azure AI Foundry Agent core implementation using Microsoft Agent Framework.

This module provides integration between Microsoft Agent Framework and Azure services
(Functions and Logic Apps) as agent tools.
"""

import logging
from typing import Any, Callable, Dict, List, Optional

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool
from azure.identity import DefaultAzureCredential
from pydantic import BaseModel, Field

from src.abstractions.azure_functions import AzureFunctionsClient, FunctionConfig
from src.abstractions.logic_apps import LogicAppsClient, LogicAppConfig

logger = logging.getLogger(__name__)


class AgentConfig(BaseModel):
    """Configuration for the AI Foundry agent using Microsoft Agent Framework.

    Attributes:
        project_endpoint: Azure AI Foundry project endpoint URL.
        use_managed_identity: Whether to use Azure Managed Identity for authentication.
        model_name: Name of the model deployment to use (e.g., "gpt-4", "gpt-35-turbo").
        instructions: System instructions for the agent.
    """

    project_endpoint: str = Field(
        ..., description="Azure AI Foundry project endpoint URL"
    )
    use_managed_identity: bool = Field(
        True, description="Use Azure Managed Identity for authentication"
    )
    model_name: str = Field("gpt-4", description="Model deployment name to use")
    instructions: str = Field(
        "You are a helpful AI assistant with access to Azure tools.",
        description="System instructions for the agent",
    )


class FoundryAgent:
    """Azure AI Foundry Agent using Microsoft Agent Framework.

    This agent uses the official Microsoft Agent Framework SDK to create agents
    that can use Azure Functions and Logic Apps as tools.

    Example:
        >>> from azure.identity import DefaultAzureCredential
        >>> config = AgentConfig(
        ...     project_endpoint="https://my-project.api.azureml.ms",
        ...     model_name="gpt-4"
        ... )
        >>> agent = FoundryAgent(config)
        >>>
        >>> # Register Azure Function as tool
        >>> function_config = FunctionConfig(
        ...     function_url="https://myapp.azurewebsites.net/api/process",
        ...     function_key="key123"
        ... )
        >>> agent.register_azure_function_tool("process_data", function_config)
        >>>
        >>> # Create and run agent
        >>> agent_id = agent.create_agent()
        >>> response = agent.run_agent(agent_id, "Process this data: [1, 2, 3]")
    """

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the Foundry Agent with Microsoft Agent Framework.

        Args:
            config: Configuration for the agent.
        """
        self.config = config
        self._tools: Dict[str, Callable] = {}
        self._function_tools: List[FunctionTool] = []

        # Initialize Azure AI Project Client
        credential = DefaultAzureCredential()
        self._client = AIProjectClient(
            endpoint=self.config.project_endpoint, credential=credential
        )

        logger.info(
            f"Initialized Foundry Agent with project: {self.config.project_endpoint}"
        )

    def register_azure_function_tool(
        self, name: str, config: FunctionConfig, description: Optional[str] = None
    ) -> None:
        """Register an Azure Function as an agent tool.

        Args:
            name: Name for the tool.
            config: Configuration for the Azure Function.
            description: Optional description of what the function does.
        """
        client = AzureFunctionsClient(config)

        def tool_function(**kwargs: Any) -> Dict[str, Any]:
            """Wrapper function for Azure Function invocation."""
            logger.info(f"Invoking Azure Function tool: {name}")
            try:
                result = client.invoke_function(kwargs)
                logger.info(f"Azure Function tool '{name}' executed successfully")
                return result
            except Exception as e:
                logger.error(f"Azure Function tool '{name}' failed: {str(e)}")
                return {"error": str(e), "status": "failed"}

        # Store the function
        tool_function.__name__ = name
        self._tools[name] = tool_function

        # Create function tool definition for Agent Framework
        function_tool = FunctionTool(
            name=name,
            description=description
            or f"Azure Function tool: {name} - Invokes Azure Function at {config.function_url}",
            parameters={
                "type": "object",
                "properties": {
                    "payload": {
                        "type": "object",
                        "description": "JSON payload to send to the Azure Function",
                    }
                },
                "required": ["payload"],
            },
        )
        self._function_tools.append(function_tool)

        logger.info(f"Registered Azure Function tool: {name}")

    def register_logic_app_tool(
        self, name: str, config: LogicAppConfig, description: Optional[str] = None
    ) -> None:
        """Register a Logic App workflow as an agent tool.

        Args:
            name: Name for the tool.
            config: Configuration for the Logic App.
            description: Optional description of what the workflow does.
        """
        client = LogicAppsClient(config)

        def tool_function(**kwargs: Any) -> Dict[str, Any]:
            """Wrapper function for Logic App workflow invocation."""
            logger.info(f"Invoking Logic App tool: {name}")
            try:
                result = client.trigger_workflow(kwargs)
                logger.info(f"Logic App tool '{name}' executed successfully")
                return result
            except Exception as e:
                logger.error(f"Logic App tool '{name}' failed: {str(e)}")
                return {"error": str(e), "status": "failed"}

        # Store the function
        tool_function.__name__ = name
        self._tools[name] = tool_function

        # Create function tool definition for Agent Framework
        function_tool = FunctionTool(
            name=name,
            description=description
            or f"Logic App workflow tool: {name} - Triggers workflow at {config.workflow_url}",
            parameters={
                "type": "object",
                "properties": {
                    "payload": {
                        "type": "object",
                        "description": "JSON payload to send to the Logic App workflow",
                    }
                },
                "required": ["payload"],
            },
        )
        self._function_tools.append(function_tool)

        logger.info(f"Registered Logic App tool: {name}")

    def register_custom_tool(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters: Dict[str, Any],
    ) -> None:
        """Register a custom Python function as a tool.

        Args:
            name: Name of the tool.
            function: Callable Python function.
            description: Description of what the tool does.
            parameters: JSON schema for the function parameters.
        """
        self._tools[name] = function

        function_tool = FunctionTool(
            name=name, description=description, parameters=parameters
        )
        self._function_tools.append(function_tool)

        logger.info(f"Registered custom tool: {name}")

    def create_agent(self, name: Optional[str] = None) -> str:
        """Create an agent with registered tools using Microsoft Agent Framework.

        Args:
            name: Optional name for the agent.

        Returns:
            The agent ID.
        """
        agent_name = name or "Azure Tools Agent"

        logger.info(f"Creating agent: {agent_name}")

        # Create agent with tools
        agent = self._client.agents.create_agent(
            model=self.config.model_name,
            name=agent_name,
            instructions=self.config.instructions,
            tools=self._function_tools,
            tool_resources={},
        )

        logger.info(f"Agent created with ID: {agent.id}")
        return agent.id

    def run_agent(
        self, agent_id: str, user_message: str, thread_id: Optional[str] = None
    ) -> str:
        """Run the agent with a user message.

        Args:
            agent_id: The ID of the agent to run.
            user_message: The user's message.
            thread_id: Optional thread ID for conversation continuity.

        Returns:
            The agent's response text.
        """
        logger.info(f"Running agent {agent_id} with message: {user_message[:50]}...")

        # Create or use existing thread
        if not thread_id:
            thread = self._client.agents.create_thread()
            thread_id = thread.id
            logger.info(f"Created new thread: {thread_id}")

        # Add message to thread
        self._client.agents.create_message(
            thread_id=thread_id, role="user", content=user_message
        )

        # Run the agent
        run = self._client.agents.create_and_process_run(
            thread_id=thread_id, agent_id=agent_id
        )

        logger.info(f"Agent run completed with status: {run.status}")

        # Get messages
        messages = self._client.agents.list_messages(thread_id=thread_id)

        # Return the last assistant message
        for message in messages:
            if message.role == "assistant":
                content = message.content[0]
                if hasattr(content, "text"):
                    return content.text.value

        return "No response generated"

    def list_tools(self) -> List[str]:
        """Get a list of all registered tools.

        Returns:
            List of tool names.
        """
        return list(self._tools.keys())

    def delete_agent(self, agent_id: str) -> None:
        """Delete an agent.

        Args:
            agent_id: The ID of the agent to delete.
        """
        self._client.agents.delete_agent(agent_id)
        logger.info(f"Deleted agent: {agent_id}")
