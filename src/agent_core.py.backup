"""
Azure AI Foundry Agent core implementation.

This module provides the core agent framework for integrating Azure Functions
and Logic Apps as tools within an AI agent workflow.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Union

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from pydantic import BaseModel, Field

from src.abstractions.azure_functions import AzureFunctionsClient, FunctionConfig
from src.abstractions.logic_apps import LogicAppsClient, LogicAppConfig

logger = logging.getLogger(__name__)


class AgentConfig(BaseModel):
    """Configuration for the AI Foundry agent.

    Attributes:
        endpoint: Azure AI Foundry endpoint URL.
        api_key: Optional API key for authentication.
        model_name: Name of the model to use (e.g., "gpt-4", "gpt-35-turbo").
        use_managed_identity: Whether to use Azure Managed Identity.
        system_prompt: System prompt to initialize the agent.
    """

    endpoint: str = Field(..., description="Azure AI Foundry endpoint URL")
    api_key: Optional[str] = Field(None, description="API key for authentication")
    model_name: str = Field("gpt-4", description="Model name to use")
    use_managed_identity: bool = Field(
        False, description="Use Azure Managed Identity for authentication"
    )
    system_prompt: str = Field(
        "You are a helpful AI assistant with access to Azure tools.",
        description="System prompt for the agent",
    )


class Tool(BaseModel):
    """Represents a tool that can be used by the agent.

    Attributes:
        name: Name of the tool.
        description: Description of what the tool does.
        function: Callable function that implements the tool.
        parameters_schema: Optional JSON schema for tool parameters.
    """

    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of the tool")
    function: Any = Field(..., description="Callable function")
    parameters_schema: Optional[Dict[str, Any]] = Field(
        None, description="JSON schema for tool parameters"
    )

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True


class FoundryAgent:
    """Azure AI Foundry Agent with integrated Azure tools.

    This agent can use Azure Functions and Logic Apps as tools to accomplish
    tasks, providing a bridge between AI capabilities and Azure services.

    Example:
        >>> config = AgentConfig(
        ...     endpoint="https://myendpoint.openai.azure.com",
        ...     api_key="your-api-key",
        ...     model_name="gpt-4"
        ... )
        >>> agent = FoundryAgent(config)
        >>>
        >>> # Register an Azure Function tool
        >>> function_config = FunctionConfig(
        ...     function_url="https://myapp.azurewebsites.net/api/myfunction",
        ...     function_key="key123"
        ... )
        >>> agent.register_azure_function("data_processor", function_config)
        >>>
        >>> # Run the agent
        >>> response = agent.run("Process this data: [1, 2, 3, 4, 5]")
    """

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the Foundry Agent.

        Args:
            config: Configuration for the agent.
        """
        self.config = config
        self._tools: Dict[str, Tool] = {}
        self._conversation_history: List[Union[SystemMessage, UserMessage]] = []

        # Initialize the Azure AI client
        if self.config.use_managed_identity:
            credential = DefaultAzureCredential()
            self._client = ChatCompletionsClient(
                endpoint=self.config.endpoint, credential=credential
            )
            logger.info("Initialized agent with managed identity")
        elif self.config.api_key:
            self._client = ChatCompletionsClient(
                endpoint=self.config.endpoint,
                credential=AzureKeyCredential(self.config.api_key),
            )
            logger.info("Initialized agent with API key")
        else:
            raise ValueError("Either api_key or use_managed_identity must be provided")

        # Add system prompt
        self._conversation_history.append(
            SystemMessage(content=self.config.system_prompt)
        )
        logger.info(f"Agent initialized with model: {self.config.model_name}")

    def register_tool(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters_schema: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Register a custom tool with the agent.

        Args:
            name: Name of the tool.
            function: Callable function that implements the tool.
            description: Description of what the tool does.
            parameters_schema: Optional JSON schema for tool parameters.
        """
        tool = Tool(
            name=name,
            description=description,
            function=function,
            parameters_schema=parameters_schema,
        )
        self._tools[name] = tool
        logger.info(f"Registered tool: {name}")

    def register_azure_function(
        self, name: str, config: FunctionConfig, description: Optional[str] = None
    ) -> None:
        """Register an Azure Function as a tool.

        Args:
            name: Name to give the tool.
            config: Configuration for the Azure Function.
            description: Optional description of what the function does.
        """
        client = AzureFunctionsClient(config)

        def function_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
            """Wrapper function for Azure Function invocation."""
            return client.invoke_function(payload)

        self.register_tool(
            name=name,
            function=function_tool,
            description=description or f"Azure Function tool: {name}",
        )
        logger.info(f"Registered Azure Function tool: {name}")

    def register_logic_app(
        self, name: str, config: LogicAppConfig, description: Optional[str] = None
    ) -> None:
        """Register a Logic App workflow as a tool.

        Args:
            name: Name to give the tool.
            config: Configuration for the Logic App.
            description: Optional description of what the workflow does.
        """
        client = LogicAppsClient(config)

        def workflow_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
            """Wrapper function for Logic App workflow invocation."""
            return client.trigger_workflow(payload)

        self.register_tool(
            name=name,
            function=workflow_tool,
            description=description or f"Logic App workflow tool: {name}",
        )
        logger.info(f"Registered Logic App tool: {name}")

    def list_tools(self) -> List[str]:
        """Get a list of all registered tools.

        Returns:
            List of tool names.
        """
        return list(self._tools.keys())

    def get_tool_description(self, tool_name: str) -> Optional[str]:
        """Get the description of a specific tool.

        Args:
            tool_name: Name of the tool.

        Returns:
            Tool description or None if tool not found.
        """
        tool = self._tools.get(tool_name)
        return tool.description if tool else None

    def invoke_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke a registered tool.

        Args:
            tool_name: Name of the tool to invoke.
            parameters: Parameters to pass to the tool.

        Returns:
            Result from the tool invocation.

        Raises:
            ValueError: If the tool is not found.
            Exception: If the tool invocation fails.
        """
        tool = self._tools.get(tool_name)
        if not tool:
            error_msg = (
                f"Tool '{tool_name}' not found. Available tools: {self.list_tools()}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"Invoking tool: {tool_name}")
        logger.debug(f"Tool parameters: {parameters}")

        try:
            result = tool.function(parameters)
            logger.info(f"Tool '{tool_name}' invoked successfully")
            return result
        except Exception as e:
            logger.error(f"Tool '{tool_name}' invocation failed: {str(e)}")
            raise

    def run(self, user_message: str, max_iterations: int = 5) -> str:
        """Run the agent with a user message.

        This is a simplified implementation that demonstrates the agent flow.
        In a production implementation, this would include tool calling logic
        and iterative reasoning.

        Args:
            user_message: The user's input message.
            max_iterations: Maximum number of reasoning iterations.

        Returns:
            The agent's response.
        """
        logger.info("Running agent with user message")
        logger.debug(f"User message: {user_message}")

        # Add user message to history
        self._conversation_history.append(UserMessage(content=user_message))

        try:
            # Note: This is a simplified implementation
            # A full implementation would include tool calling and function execution
            response = self._client.complete(
                messages=self._conversation_history, model=self.config.model_name
            )

            assistant_message = response.choices[0].message.content
            logger.info("Agent response generated successfully")

            return assistant_message

        except Exception as e:
            logger.error(f"Agent execution failed: {str(e)}")
            raise

    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self._conversation_history = [SystemMessage(content=self.config.system_prompt)]
        logger.info("Conversation history reset")
