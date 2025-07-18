.. _user_guide_simulation:

========================
Concept: Simulation
========================

How do you know if your agent is reliable? The **Simulation** module is CogniCoreAI's answer to this question. It provides a powerful framework for **behavioral testing**, allowing you to verify that your agent behaves as expected in complex, multi-turn conversations.

This goes beyond traditional testing by evaluating the agent's reasoning and decision-making process.

The Three Pillars of Simulation
-------------------------------

The simulation framework is built on three core concepts:

1.  ``Assertion``  
    An assertion is a single, verifiable condition that must be true for a test to pass. It is a class with an ``evaluate(history)`` method that returns ``True`` or ``False``. CogniCoreAI provides built-in assertions like:  
    - ``ToolUsedAssertion(tool_name)``: Checks if a specific tool was ever called.  
    - ``ResponseContainsAssertion(text)``: Checks if the agent's final answer includes a certain piece of text.

2.  ``Scenario``  
    A scenario bundles everything needed for a single behavioral test case:  
    - A unique ``name``.  
    - A list of ``steps``, which are the user messages to send to the agent in sequence.  
    - A list of ``Assertion``\ s that will be evaluated against the agent's final memory state.

3.  ``Simulator``  
    The ``Simulator`` is the engine that runs the tests. You give it an agent and a list of scenarios. For each scenario, it will:  
    a. Reset the agent's memory for a clean slate.  
    b. Run through the conversational steps.  
    c. Evaluate every assertion defined in the scenario.  
    d. Generate a detailed ``SimulationResult`` report.

Putting It All Together
-----------------------

This example demonstrates how the pieces fit together to create a robust test.

.. code-block:: python

   from cognicoreai import (
       Agent, Simulator, Scenario,
       ToolUsedAssertion, ResponseContainsAssertion,
       # ... other components
   )

   # 1. Define the Scenario with steps and assertions
   my_scenario = Scenario(
       name="Check if agent uses calculator correctly",
       steps=["What is the result of 50 times 3?"],
       assertions=[
           ToolUsedAssertion("calculator"),
           ResponseContainsAssertion("150")
       ]
   )

   # 2. Set up the agent to be tested
   my_agent = Agent(...) 

   # 3. Run the simulation
   simulator = Simulator()
   results = simulator.run(my_agent, [my_scenario])

   # 4. Check the report
   for result in results:
       if result.passed:
           print(f"Scenario '{result.scenario_name}' PASSED!")
       else:
           print(f"Scenario '{result.scenario_name}' FAILED!")

By building a suite of these simulations, you can confidently make changes and add new features to your agent, knowing that you can always verify its core behaviors have not been broken.
