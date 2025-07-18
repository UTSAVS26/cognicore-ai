.. _how_to_create_tool:

========================
Create a Custom Tool
========================

The true power of an agent comes from the tools it can use. CogniCoreAi is designed to make adding new tools as simple as possible. This guide will show you how to create a custom tool to get the current date and time.

The Core Concept
----------------

Any custom tool is a Python class that inherits from ``cognicoreai.Tool`` and correctly implements three things:

1.  A ``name`` property: A unique, single-word identifier for the tool.
2.  A ``description`` property: A clear, natural language explanation of what the tool does. The LLM uses this to decide when to use the tool.
3.  A ``run`` method: The actual Python code that gets executed.

Step 1: Define the Tool Class
-----------------------------

Let's create a tool that returns the current date and time. Create a new class, ``DateTimeTool``, that inherits from ``Tool``.

.. code-block:: python
   :linenos:

   import datetime
   from cognicoreai import Tool

   class DateTimeTool(Tool):
       """A tool to get the current date and time."""

       @property
       def name(self) -> str:
           return "get_current_datetime"

       @property
       def description(self) -> str:
           return "Returns the current date and time. It takes no input."

       def run(self, tool_input: str) -> str:
           # This tool ignores the input, but it's good practice to include
           # the parameter in the method signature to match the base class.
           return datetime.datetime.now().isoformat()


Step 2: Use the Tool in an Agent
--------------------------------

Now, you can import your new tool and add it to the agent's tool list during initialization.

.. code-block:: python
   :linenos:
   :emphasize-lines: 4, 11

   from cognicoreai import Agent, OpenAI_LLM, VolatileMemory, CalculatorTool
   # Import your new custom tool
   from your_project_file import DateTimeTool 

   # 1. Initialize the LLM and Memory
   llm = OpenAI_LLM()
   memory = VolatileMemory()

   # 2. Create a list of all tools the agent can use
   tools = [CalculatorTool(), DateTimeTool()]
   
   # 3. Create the agent
   agent = Agent(llm, memory, tools)

   # 4. Chat with the agent and ask it to use the new tool
   # The LLM will see "get_current_datetime" in its list of available tools
   # and will know to call it when asked about the time.
   response = agent.chat("What time is it right now?")
   print(response)

And that's it! The agent will now have the ability to report the current date and time by executing your custom Python code.