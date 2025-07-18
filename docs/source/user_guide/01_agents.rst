.. _user_guide_agent:

=====================
Concept: The Agent
=====================

The **Agent** is the heart of the CogniCore framework. It is the central orchestrator that brings all other components together to create intelligent, interactive behavior. Think of the Agent as the "brain" of the operation.

Core Responsibilities
---------------------

The ``cognicore.Agent`` class has several key responsibilities:

1.  **Managing the Conversation Flow:** The Agent controls the primary "Reason-Act" loop. When it receives input, it decides whether to respond directly, use a tool, or perform another action.
2.  **Interacting with the LLM:** It formats the current conversation history and available tools into a prompt, sends it to the configured LLM (via the LLM abstraction), and processes the response.
3.  **Coordinating Memory:** It adds user inputs and its own responses back into the memory module, ensuring the conversation's context is maintained.
4.  **Executing Tools:** When the LLM decides to use a tool, the Agent uses its ``ToolHandler`` to execute the correct tool and feed the result back into the conversation for the LLM to process further.

Composition over Inheritance
----------------------------

A key design principle in CogniCore is "composition over inheritance." The Agent is not a monolithic entity; it is *composed* of other, smaller components at runtime.

When you initialize an Agent, you provide it with the pieces it needs to function:

.. code-block:: python

   from cognicore import Agent, OpenAI_LLM, VolatileMemory, CalculatorTool

   # 1. The Agent is given an LLM instance to power its reasoning.
   llm = OpenAI_LLM()

   # 2. It is given a Memory instance to store the conversation.
   memory = VolatileMemory()

   # 3. It is given a list of Tools it can use.
   tools = [CalculatorTool()]

   # The agent is "composed" of these parts.
   agent = Agent(
       llm=llm,
       memory=memory,
       tools=tools
   )

This approach makes the framework incredibly flexible. You can easily swap out any component—for example, replacing ``VolatileMemory`` with a persistent database memory or replacing ``OpenAI_LLM`` with a different model provider—without changing the Agent's internal logic.