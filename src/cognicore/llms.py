"""
LLM Abstraction Module for CogniCore.

This module provides a generic interface for interacting with various Large
Language Models (LLMs). The core component is the `BaseLLM` abstract class,
which defines a standard "contract" that all LLM provider implementations
must follow.

This abstraction decouples the `Agent` from any specific LLM provider (like
OpenAI), making the framework highly modular and extensible. To add support
for a new model, one simply needs to create a new class that inherits from
`BaseLLM` and implements the `get_completion` method.
"""

import abc
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# The client library for our first implementation
import openai

# Import the core Message type from the memory module
from .memory import Message

# --- Data Structures for Standardized LLM Interaction ---


@dataclass
class ToolCall:
    """
    A standardized data structure representing a tool call requested by an LLM.

    This class ensures that the Agent receives tool call information in a
    consistent format, regardless of the underlying LLM provider.

    Attributes:
        id (str): A unique identifier for this specific tool call.
        function_name (str): The name of the function/tool to be called.
        arguments (str): A JSON string representing the arguments for the function.
    """

    id: str
    function_name: str
    arguments: str


@dataclass
class LLMResponse:
    """
    A standardized data structure for the response from any LLM.

    This class abstracts away the provider-specific response object, giving
    the Agent a clean and predictable object to work with.

    Attributes:
        content (Optional[str]): The direct text response from the model. This is
            None if the model decides to call a tool instead of responding.
        tool_calls (Optional[List[ToolCall]]): A list of tool calls requested
            by the model. This is None if the model provides a direct text response.
        raw_response_message (Any): The original, unaltered message object from
            the LLM provider's response. This is useful for logging the exact
            model output back into memory.
    """

    content: Optional[str]
    tool_calls: Optional[List[ToolCall]]
    raw_response_message: Any


# --- LLM Abstraction and Implementation ---


class BaseLLM(abc.ABC):
    """
    Abstract Base Class for all LLM clients.

    This class defines the "contract" for how the CogniCore Agent interacts
    with an LLM. Any class that provides access to an LLM must inherit from
    this class and implement the `get_completion` method.
    """

    @abc.abstractmethod
    def get_completion(
        self, messages: List[Message], tools: List[Dict[str, Any]]
    ) -> LLMResponse:
        """
        Sends a request to the LLM and returns a standardized response.

        Args:
            messages (List[Message]): The sequence of messages forming the
                conversation history.
            tools (List[Dict[str, Any]]): The definitions of tools available
                for the LLM to use.

        Returns:
            LLMResponse: A standardized response object containing the model's
                         reply and any requested tool calls.
        """
        raise NotImplementedError


class OpenAI_LLM(BaseLLM):
    """
    A concrete implementation of `BaseLLM` for OpenAI's chat models.

    This class handles all the specifics of communicating with the OpenAI API.
    """

    def __init__(self, model: str = "gpt-4-turbo", api_key: Optional[str] = None):
        """
        Initializes the OpenAI client.

        Args:
            model (str): The identifier for the OpenAI model to be used
                         (e.g., "gpt-4-turbo", "gpt-3.5-turbo").
            api_key (Optional[str]): The OpenAI API key. If not provided, it
                                     will fall back to the `OPENAI_API_KEY`
                                     environment variable.
        """
        self.model = model
        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def get_completion(
        self, messages: List[Message], tools: List[Dict[str, Any]]
    ) -> LLMResponse:
        """
        Implements the LLM call specifically for the OpenAI API.

        It translates the OpenAI-specific response object into the framework's
        standard `LLMResponse` format.
        """
        # The API call is made differently if tools are available
        if tools:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model, messages=messages
            )

        response_message = response.choices[0].message

        # Check if the model decided to call tools
        raw_tool_calls = response_message.tool_calls
        parsed_tool_calls = None
        if raw_tool_calls:
            parsed_tool_calls = [
                ToolCall(
                    id=tc.id,
                    function_name=tc.function.name,
                    arguments=tc.function.arguments,
                )
                for tc in raw_tool_calls
            ]

        return LLMResponse(
            content=response_message.content,
            tool_calls=parsed_tool_calls,
            raw_response_message=response_message,
        )
