"""
Integration tests for the Agent class.

These tests use mocking to simulate LLM behavior and validate the agent's
entire reasoning and tool-use loop without making real API calls. This ensures
tests are fast, deterministic, and free.
"""

import unittest
from unittest.mock import MagicMock

# Import all the components we need to assemble an agent
from cognicoreai import (
    Agent,
    BaseLLM,
    CalculatorTool,
    LLMResponse,
    ToolCall,
    VolatileMemory,
)


class TestAgentIntegration(unittest.TestCase):
    """Test suite for the Agent's core logic."""

    def setUp(self):
        """Set up the components needed for an agent before each test."""
        # 1. Create a mock LLM object that we can control
        self.mock_llm = MagicMock(spec=BaseLLM)

        # 2. Create real instances of memory and tools
        self.memory = VolatileMemory()
        self.tools = [CalculatorTool()]

        # 3. Create the agent instance with the mocked LLM
        self.agent = Agent(
            llm=self.mock_llm,
            memory=self.memory,
            tools=self.tools,
            system_prompt="You are a helpful calculator bot.",
        )

    def test_initialization_with_system_prompt(self):
        """Test that the agent initializes memory with the system prompt."""
        history = self.memory.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["role"], "system")
        self.assertEqual(history[0]["content"], "You are a helpful calculator bot.")

    def test_simple_chat_no_tools(self):
        """Test a simple conversation without any tool calls."""
        # Configure the mock LLM to return a simple text response
        mocked_response = LLMResponse(
            content="Hello! How can I help you today?",
            tool_calls=None,
            raw_response_message={
                "role": "assistant",
                "content": "Hello! How can I help you today?",
            },
        )
        self.mock_llm.get_completion.return_value = mocked_response

        # Call the agent
        user_input = "Hi there!"
        agent_response = self.agent.chat(user_input)

        # Assertions
        # Check that the agent returned the correct content
        self.assertEqual(agent_response, "Hello! How can I help you today?")

        # Check that the LLM was called exactly once
        self.mock_llm.get_completion.assert_called_once()

        # Check that the memory contains the full conversation
        history = self.memory.get_history()
        self.assertEqual(len(history), 3)  # system, user, assistant
        self.assertEqual(history[1]["content"], user_input)
        self.assertEqual(history[2]["content"], "Hello! How can I help you today?")

    def test_chat_with_tool_use_cycle(self):
        """Test the full 'reason-act' cycle where the agent uses a tool."""
        # --- Configure the mock for a two-step conversation ---

        # 1. The first LLM call decides to use the calculator tool
        first_response = LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call_123",
                    function_name="calculator",
                    arguments='{"tool_input": "4 * 8"}',
                )
            ],
            raw_response_message={
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call_123",
                        "function": {
                            "name": "calculator",
                            "arguments": '{"tool_input": "4 * 8"}',
                        },
                    }
                ],
            },
        )

        # 2. The second LLM call provides a natural language response
        # after seeing the tool's output
        second_response = LLMResponse(
            content="Of course. 4 times 8 is 32.",
            tool_calls=None,
            raw_response_message={
                "role": "assistant",
                "content": "Of course. 4 times 8 is 32.",
            },
        )

        # Set the mock to return these responses in sequence
        self.mock_llm.get_completion.side_effect = [first_response, second_response]

        # --- Call the agent ---
        agent_response = self.agent.chat("What is 4 * 8?")

        # --- Assertions ---
        # Assert the final response is correct
        self.assertEqual(agent_response, "Of course. 4 times 8 is 32.")

        # Assert the LLM was called twice
        self.assertEqual(self.mock_llm.get_completion.call_count, 2)

        # Assert the complete conversation history is stored correctly in memory
        history = self.memory.get_history()
        self.assertEqual(len(history), 5)

        self.assertEqual(history[0]["role"], "system")
        self.assertEqual(history[1]["role"], "user")
        self.assertEqual(history[1]["content"], "What is 4 * 8?")
        self.assertEqual(history[2]["role"], "assistant")  # Model's decision
        self.assertIsNotNone(history[2]["tool_calls"])
        self.assertEqual(history[3]["role"], "tool")  # The tool's output
        self.assertEqual(history[3]["tool_call_id"], "call_123")
        self.assertEqual(history[3]["content"], "32.0")  # Output from CalculatorTool
        self.assertEqual(history[4]["role"], "assistant")  # Final text response
        self.assertEqual(history[4]["content"], "Of course. 4 times 8 is 32.")
