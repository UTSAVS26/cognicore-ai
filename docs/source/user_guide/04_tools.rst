.. _user_guide_tools:

================
Concept: Tools
================

By default, an LLM's knowledge is limited to the data it was trained on. **Tools** are what give a CogniCoreAI agent the ability to break free from these limitations and interact with the real world. A tool is a piece of code that allows an agent to get new information or perform an action.

Examples of tools include:

*   A calculator to perform math.
*   A search engine to get up-to-date information.
*   An API client to check the weather or book a flight.

The `Tool` Contract
-------------------

Every tool in CogniCoreAI must inherit from the ``cognicoreai.tools.Tool`` abstract base class. This contract ensures every tool provides the critical information the LLM needs to use it effectively.

1.  ``name`` **property**: A unique, simple name for the tool (e.g., ``"web_search"``). This is what the LLM will use to identify the tool it wants to call.
2.  ``description`` **property**: This is the most important part for the LLM. It's a natural language description of what the tool does, what it's good for, and what its input should look like. A good description is essential for the agent to reason correctly about when to use the tool.
3.  ``run(tool_input)`` **method**: The actual Python function that gets executed when the tool is called.

Example: The `CalculatorTool`
-----------------------------

Let's look at the built-in ``CalculatorTool`` as an example.

.. code-block:: python

   from cognicoreai import Tool

   class CalculatorTool(Tool):
       @property
       def name(self) -> str:
           return "calculator"

       @property
       def description(self) -> str:
           # This description is sent to the LLM in the prompt.
           return (
               "A calculator tool for basic arithmetic. "
               "Input should be a simple mathematical expression, like '2 + 2' or '10 * 4'."
           )
       
       def run(self, tool_input: str) -> str:
           # Logic to evaluate the math expression goes here...
           ...

When an agent is initialized with this tool, its description is formatted and included in the system prompt sent to the LLM. When a user asks "What is 10 times 4?", the LLM sees the ``calculator`` tool's description and understands that it is the right tool for the job. It then tells the Agent to execute ``calculator.run("10 * 4")``.