.. _user_guide_memory:

==================
Concept: Memory
==================

For an agent to have a coherent conversation, it must remember what has been said previously. The **Memory** system in CogniCore is responsible for storing, retrieving, and managing the conversation history.

The `BaseMemory` Contract
-------------------------

Like the LLM system, the memory system is built on an abstraction: the ``cognicore.memory.BaseMemory`` class. This ensures that the ``Agent`` can interact with any type of memory store in a consistent way. The ``BaseMemory`` contract requires all memory classes to implement:

*   ``add_message(message)``: Adds a new message to the history.
*   ``get_history()``: Retrieves the full list of messages.
*   ``clear()``: Wipes the entire history.

The `Message` Structure
-----------------------

All messages stored in memory follow a consistent structure, defined by the ``cognicore.memory.Message`` typed dictionary. A message has two keys:

*   ``role``: Who is speaking. This can be ``"system"``, ``"user"``, ``"assistant"``, or ``"tool"``.
*   ``content``: The text of the message.

Volatile vs. Persistent Memory
------------------------------

CogniCore comes with a simple, default memory implementation:

*   **``VolatileMemory``**: Stores the conversation history in a list in your computer's RAM. This is fast and simple, but the history is **lost** as soon as your script finishes. It's perfect for development and testing.

.. code-block:: python

   from cognicore import VolatileMemory

   # History is stored in RAM and will be cleared on exit.
   memory = VolatileMemory()
   agent = Agent(memory=memory, ...)

The ``BaseMemory`` abstraction makes it straightforward to implement your own **persistent memory** backends. For example, you could create a ``FileMemory`` class that saves the history to a JSON file or a ``DatabaseMemory`` class that connects to a SQL database, allowing conversations to be resumed across multiple sessions.