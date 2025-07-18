"""
Behavioral Simulation and Evaluation Module for CogniCore.

This module provides the tools to test an agent's behavior against predefined
scenarios. It allows developers to verify not just that individual components
work, but that the agent as a whole reasons and acts as expected in a given
conversational context.

The workflow is:
1. Define one or more `Assertion`s (conditions for success).
2. Create a `Scenario` that includes conversational steps and assertions.
3. Run the `Scenario` using the `Simulator`.
"""

import abc
from typing import Dict, List, NamedTuple

from .agents import Agent
from .memory import Message

# --- Assertion Components ---


class Assertion(abc.ABC):
    """
    Abstract Base Class for all assertions.

    An assertion is a rule that evaluates to True or False based on the
    agent's conversation history after a scenario is run.
    """

    @abc.abstractmethod
    def evaluate(self, history: List[Message]) -> bool:
        """
        Evaluates the assertion against the conversation history.

        Args:
            history (List[Message]): The complete conversation history from the
                                     agent's memory.

        Returns:
            bool: True if the assertion passes, False otherwise.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class ToolUsedAssertion(Assertion):
    """Asserts that a specific tool was called at least once."""

    def __init__(self, tool_name: str):
        """
        Args:
            tool_name (str): The name of the tool to check for.
        """
        self.tool_name = tool_name

    def evaluate(self, history: List[Message]) -> bool:
        for message in history:
            # Tool calls are stored in 'assistant' messages
            if message["role"] == "assistant" and message.get("tool_calls"):
                for tool_call in message["tool_calls"]:
                    if tool_call["function"]["name"] == self.tool_name:
                        return True
        return False

    def __repr__(self) -> str:
        return f"<ToolUsedAssertion tool_name='{self.tool_name}'>"


class ResponseContainsAssertion(Assertion):
    """Asserts that the agent's final response contains specific text."""

    def __init__(self, expected_text: str, case_sensitive: bool = False):
        """
        Args:
            expected_text (str): The substring to look for in the final response.
            case_sensitive (bool): Whether the comparison should be case-sensitive.
        """
        self.expected_text = expected_text
        self.case_sensitive = case_sensitive

    def evaluate(self, history: List[Message]) -> bool:
        # The final response is the last message in the history
        if not history or history[-1]["role"] != "assistant":
            return False

        final_content = history[-1]["content"] or ""

        if self.case_sensitive:
            return self.expected_text in final_content
        else:
            return self.expected_text.lower() in final_content.lower()

    def __repr__(self) -> str:
        return f"<ResponseContainsAssertion text='{self.expected_text}'>"


# --- Scenario and Simulator Components ---


class Scenario:
    """
    Defines a complete, runnable test case for an agent.
    """

    def __init__(self, name: str, steps: List[str], assertions: List[Assertion]):
        """
        Args:
            name (str): A descriptive name for the scenario.
            steps (List[str]): A list of user inputs to be sent to the agent in order.
            assertions (List[Assertion]): A list of assertions to check after the
                                          conversation is complete.
        """
        self.name = name
        self.steps = steps
        self.assertions = assertions


class SimulationResult(NamedTuple):
    """A data structure to hold the results of a single scenario simulation."""

    scenario_name: str
    passed: bool
    assertion_results: Dict[str, bool]
    final_history: List[Message]


class Simulator:
    """
    The engine that runs scenarios against an agent and reports results.
    """

    def run(self, agent: Agent, scenarios: List[Scenario]) -> List[SimulationResult]:
        """
        Executes a list of scenarios against a given agent.

        Args:
            agent (Agent): The agent instance to test.
            scenarios (List[Scenario]): A list of scenarios to run.

        Returns:
            List[SimulationResult]: A list of result objects, one for each scenario.
        """
        all_results = []
        for scenario in scenarios:
            # Reset the agent's memory before each scenario for isolation
            agent.memory.clear()
            # Re-add the system prompt
            agent.memory.add_message({"role": "system", "content": agent.system_prompt})

            # Run the conversational steps
            for user_input in scenario.steps:
                agent.chat(user_input)

            # Get the final state of the agent's memory
            final_history = agent.memory.get_history()

            # Evaluate all assertions for the scenario
            assertion_results = {
                repr(assertion): assertion.evaluate(final_history)
                for assertion in scenario.assertions
            }

            # The scenario passes only if all its assertions pass
            scenario_passed = all(assertion_results.values())

            all_results.append(
                SimulationResult(
                    scenario_name=scenario.name,
                    passed=scenario_passed,
                    assertion_results=assertion_results,
                    final_history=final_history,
                )
            )

        return all_results
