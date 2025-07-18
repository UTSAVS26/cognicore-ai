.. _user_guide_llm:

================
Concept: LLMs
================

A conversational agent is powered by a Large Language Model (LLM). However, different LLM providers (like OpenAI, Google, Anthropic) have different APIs and response formats. To handle this, CogniCore uses an **LLM Abstraction Layer**.

This layer decouples the ``Agent`` from any specific LLM provider, making the framework highly modular and future-proof.

The `BaseLLM` Contract
----------------------

The core of the abstraction is the ``cognicore.llms.BaseLLM`` abstract base class. This class defines a "contract" that any LLM provider must follow. It requires one essential method:

*   ``get_completion(messages, tools)``: This method takes the conversation history and available tools, sends them to the specific LLM API, and returns a standardized response.

The `LLMResponse` Data Structure
--------------------------------

To ensure the ``Agent`` receives data in a consistent format, the ``get_completion`` method must return an instance of ``cognicore.llms.LLMResponse``. This is a simple data class that standardizes the output from any model. It contains:

*   ``content``: The text response from the model.
*   ``tool_calls``: A list of any tools the model requested to use.
*   ``raw_response_message``: The original, provider-specific response object, which is useful for logging.

Concrete Implementations
------------------------

CogniCore provides an out-of-the-box implementation for OpenAI models with the ``cognicore.llms.OpenAI_LLM`` class.

.. code-block:: python

   from cognicore.llms import BaseLLM, LLMResponse, OpenAI_LLM

   # This class fulfills the BaseLLM contract.
   llm = OpenAI_LLM(model="gpt-4-turbo")

   # The Agent doesn't care that it's an OpenAI_LLM; it only knows
   # that it's a BaseLLM and has a .get_completion() method.
   # agent = Agent(llm=llm, ...)

Adding support for a new LLM provider is as simple as creating a new class that inherits from ``BaseLLM`` and implements the ``get_completion`` method to call the new provider's API and format the result as an ``LLMResponse``.