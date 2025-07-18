.. _how_to_save_conversation:

=============================
Save a Conversation to a File
=============================

Agents in CogniCoreAI use a memory module to keep track of the conversation. While ``VolatileMemory`` forgets the history when your script ends, you can easily access this history and save it to a file for later analysis or to create a persistent record.

The Core Concept
----------------

The agent's memory object stores the entire conversation as a list of Python dictionaries. You can retrieve this list at any time by calling ``agent.memory.get_history()``. You can then use standard Python libraries like ``json`` to write this data to a file.

Step 1: Have a Conversation
---------------------------

First, let's create an agent and have a short conversation with it so there is something in its memory.

.. code-block:: python
   :linenos:

   from cognicoreai import Agent, OpenAI_LLM, VolatileMemory, CalculatorTool

   agent = Agent(
       llm=OpenAI_LLM(),
       memory=VolatileMemory(),
       tools=[CalculatorTool()]
   )

   agent.chat("Hi, my name is Alex.")
   agent.chat("What is 5 plus 3?")


Step 2: Retrieve and Save the History
-------------------------------------

After the conversation, the agent's memory contains a complete record. We can now get this history and save it as a JSON file.

.. code-block:: python
   :linenos:
   :emphasize-lines: 1, 6-9

   import json

   # Get the history from the agent's memory
   conversation_history = agent.memory.get_history()

   # Save the history to a file
   with open("conversation_log.json", "w") as f:
       # Use indent=2 for a nicely formatted, human-readable file
       json.dump(conversation_history, f, indent=2)

   print("Conversation saved to conversation_log.json")

After running this script, you will have a file named ``conversation_log.json`` with the following content:

.. code-block:: json

   [
     {
       "role": "system",
       "content": "You are a friendly and helpful assistant named Cogni. You have access to a calculator."
     },
     {
       "role": "user",
       "content": "Hi, my name is Alex."
     },
     {
       "role": "assistant",
       "content": "Hello Alex! It's nice to meet you. How can I help you today?"
     },
     {
       "role": "user",
       "content": "What is 5 plus 3?"
     },
     {
       "role": "assistant",
       "content": null,
       "tool_calls": [
         {
           "id": "call_123",
           "type": "function",
           "function": {
             "name": "calculator",
             "arguments": "{\"tool_input\": \"5 + 3\"}"
           }
         }
       ]
     },
     {
       "role": "tool",
       "tool_call_id": "call_123",
       "name": "calculator",
       "content": "8.0"
     },
     {
       "role": "assistant",
       "content": "5 plus 3 is 8."
     }
   ]

This simple recipe allows you to easily log, debug, or store any conversation had with your agent.