.. _how_to_write_simulation:

================================
Write a Behavioral Simulation
================================

Unit tests are great for checking if a function works, but they don't tell you if your agent *behaves* correctly. The ``Simulator`` is designed to solve this by running an agent through a scripted conversation and asserting that it acts as expected.

This guide shows how to create a simulation to verify that our agent correctly uses the ``CalculatorTool`` for a math question.

The Core Concept
----------------

A simulation consists of two parts:

1.  A ``Scenario``: Defines the user's messages and a list of conditions (``Assertion``\ s) that must be true at the end.
2.  The ``Simulator``: The engine that runs the agent through the scenario and generates a report.

Step 1: Define the Scenario
---------------------------

A scenario is just a Python object. We want to test if the agent, when asked "What is 150 / 10?", does two things:

1. It uses the ``calculator`` tool.  
2. Its final response includes the number ``15``.

.. code-block:: python
   :linenos:

   from cognicore import Scenario, ToolUsedAssertion, ResponseContainsAssertion

   # Define the assertions that must pass for the scenario to be successful
   assertions = [
       # Did the agent use the 'calculator' tool at any point?
       ToolUsedAssertion(tool_name="calculator"),
       # Does the agent's final answer contain the substring "15"?
       ResponseContainsAssertion(expected_text="15")
   ]

   # Define the scenario with a name, conversational steps, and assertions
   math_scenario = Scenario(
       name="Agent correctly uses calculator for division",
       steps=["Hey Cogni, what is 150 divided by 10?"],
       assertions=assertions
   )

Step 2: Set Up and Run the Simulator
------------------------------------

Next, create your agent as you normally would. Then, instantiate the ``Simulator`` and call its ``run`` method.

For a reproducible test, we'll use a mocked LLM, but you could also run this against the real ``OpenAI_LLM``.

.. code-block:: python
   :linenos:
   :emphasize-lines: 20-23

   from unittest.mock import MagicMock
   from cognicore import Agent, VolatileMemory, CalculatorTool, Simulator
   # We also import the scenario we just defined
   # from your_test_file import math_scenario

   # 1. Set up the agent with a mock LLM and real tools
   mock_llm = MagicMock() 
   agent = Agent(
       llm=mock_llm,
       memory=VolatileMemory(),
       tools=[CalculatorTool()]
   )

   # ... (code to configure mock_llm responses would go here) ...

   # 2. Instantiate the simulator
   simulator = Simulator()

   # 3. Run the simulation
   results = simulator.run(agent, [math_scenario])

   # 4. Print the results
   for result in results:
       print(f"Scenario '{result.scenario_name}' Passed: {result.passed}")
       for assertion, passed in result.assertion_results.items():
           print(f"  - Assertion {assertion}: {'PASS' if passed else 'FAIL'}")

This will produce a clear report, allowing you to build a suite of behavioral tests to ensure your agent remains reliable as you add more complexity.
