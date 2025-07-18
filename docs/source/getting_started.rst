.. _getting_started:

===============
Getting Started
===============

Welcome to CogniCore! This guide will walk you through the entire process of installing the framework, setting up your environment, and running your first intelligent agent in just a few minutes.

Step 1: Installation
--------------------

CogniCore is available on PyPI and can be installed with any modern Python package manager. We recommend `uv`, which is used for the development of CogniCore itself.

.. code-block:: bash

   uv pip install cognicore


Step 2: Set Your OpenAI API Key
-------------------------------

To power its reasoning, the agent needs to connect to an LLM. By default, it uses OpenAI. You must provide your API key for this to work.

The most secure and recommended way is to set an environment variable named ``OPENAI_API_KEY``.

**On Windows (Command Prompt):**

.. code-block:: bat

   set OPENAI_API_KEY=sk-YourSecretKeyHere

**On macOS / Linux:**

.. code-block:: bash

   export OPENAI_API_KEY=sk-YourSecretKeyHere

The agent will automatically detect and use this environment variable.


Step 3: Create and Run Your First Agent
---------------------------------------

Now you're ready to write some code! Create a new Python file (e.g., ``run_agent.py``) and add the following:

.. code-block:: python
   :linenos:

   from cognicore import Agent, OpenAI_LLM, VolatileMemory, CalculatorTool

   def main():
       """Sets up and runs a simple conversational agent."""
       print("Initializing agent...")
       
       # 1. Assemble the agent's components
       # The LLM provides the reasoning capabilities.
       llm = OpenAI_LLM()

       # The memory stores the conversation history.
       memory = VolatileMemory()

       # Tools give the agent new abilities.
       tools = [CalculatorTool()]

       # 2. Create the Agent instance with a system prompt
       agent = Agent(
           llm=llm,
           memory=memory,
           tools=tools,
           system_prompt="You are Cogni, a helpful assistant with a calculator."
       )

       print("Agent is ready! Ask a math question or say hello.")
       print("Type 'exit' to end the session.\n")

       # 3. Start an interactive chat loop
       while True:
           user_input = input("You: ")
           if user_input.lower() == 'exit':
               break
           
           response = agent.chat(user_input)
           print(f"Cogni: {response}\n")

   if __name__ == "__main__":
       main()


Step 4: Interact with Your Agent
--------------------------------

Save the file and run it from your terminal:

.. code-block:: bash

   python run_agent.py

You can now have a conversation. Try asking it a question that requires a tool:

.. code-block:: text

   You: What is 256 divided by 8?
   Cogni: 256 divided by 8 is 32.0.

Congratulations, you have successfully built and run your first agent with CogniCore!

Next Steps
----------

Now that you have a basic agent running, explore the rest of the documentation to learn more:

*   **User Guide**: To understand the core concepts behind how the agent works.
*   **How-To Guides**: For practical recipes to solve common problems.