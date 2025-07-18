"""
Unit tests for the simulation module.

These tests validate that the Simulator can correctly run scenarios against
a mocked agent and that Assertions evaluate correctly.
"""

import unittest
from unittest.mock import MagicMock

from cognicore import (
    Agent,
    BaseLLM,
    CalculatorTool,
    LLMResponse,
    ResponseContainsAssertion,
    Scenario,
    Simulator,
    ToolCall,
    ToolUsedAssertion,
    VolatileMemory,
)


class TestSimulation(unittest.TestCase):
    """Test suite for the Simulator and Assertions."""

    def setUp(self):
        """Set up a mocked agent and a simulator instance."""
        self.mock_llm = MagicMock(spec=BaseLLM)
        self.agent = Agent(
            llm=self.mock_llm, memory=VolatileMemory(), tools=[CalculatorTool()]
        )
        self.simulator = Simulator()

    def test_simulation_run_with_passing_and_failing_scenarios(self):
        """
        Test the simulator with two scenarios: one designed to pass
        and one designed to fail, ensuring the report is accurate.
        """
        # --- Configure the mock LLM's sequential responses ---
        # 1. Response for the "Successful Tool Use" scenario
        tool_call_response = LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call_abc",
                    function_name="calculator",
                    arguments='{"tool_input": "10 + 5"}',
                )
            ],
            raw_response_message={
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_abc",
                        "function": {
                            "name": "calculator",
                            "arguments": '{"tool_input": "10 + 5"}',
                        },
                    }
                ],
            },
        )
        final_answer_response = LLMResponse(
            content="The answer is 15.",
            tool_calls=None,
            raw_response_message={"role": "assistant", "content": "The answer is 15."},
        )
        # 2. Response for the "Failed Assertion" scenario
        simple_response = LLMResponse(
            content="Hello there!",
            tool_calls=None,
            raw_response_message={"role": "assistant", "content": "Hello there!"},
        )

        # Set the mock to return these responses in the correct order
        self.mock_llm.get_completion.side_effect = [
            tool_call_response,
            final_answer_response,
            simple_response,
        ]

        # --- Define the Scenarios ---
        scenarios = [
            Scenario(
                name="Successful Tool Use",
                steps=["What is 10 plus 5?"],
                assertions=[
                    ToolUsedAssertion(tool_name="calculator"),
                    ResponseContainsAssertion(expected_text="15"),
                ],
            ),
            Scenario(
                name="Failed Assertion",
                steps=["Hi"],
                assertions=[
                    ToolUsedAssertion(tool_name="calculator"),  # This should fail
                    ResponseContainsAssertion(
                        expected_text="world"
                    ),  # This should fail
                ],
            ),
        ]

        # --- Run the simulation ---
        results = self.simulator.run(self.agent, scenarios)

        # --- Assert the results ---
        self.assertEqual(len(results), 2)

        # Check the first scenario (should pass)
        result1 = results[0]
        self.assertEqual(result1.scenario_name, "Successful Tool Use")
        self.assertTrue(result1.passed)
        self.assertTrue(all(result1.assertion_results.values()))

        # Check the second scenario (should fail)
        result2 = results[1]
        self.assertEqual(result2.scenario_name, "Failed Assertion")
        self.assertFalse(result2.passed)
        # Check the specific assertion results
        self.assertFalse(
            result2.assertion_results["<ToolUsedAssertion tool_name='calculator'>"]
        )
        self.assertFalse(
            result2.assertion_results["<ResponseContainsAssertion text='world'>"]
        )
