<div align="center">

  <h1>🤖 CogniCore AI</h1>

  <p>
    <strong>A modular Python framework for building, testing, and deploying robust conversational AI agents.</strong>
  </p>

  <p>
    <a href="https://pypi.org/project/cognicore-ai/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/cognicore-ai.svg"></a>
    <a href="https://pypi.org/project/cognicore-ai/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/cognicore-ai.svg"></a>
    <a href="https://github.com/UTSAVS26/cognicore-ai/actions/workflows/ci.yml"><img alt="Build Status" src="https://github.com/UTSAVS26/cognicore-ai/actions/workflows/ci.yml/badge.svg"></a>
    <a href="https://github.com/UTSAVS26/cognicore-ai/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/cognicore-ai"></a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="https://cognicore-ai.readthedocs.io/en/latest/"><img alt="Documentation" src="https://img.shields.io/badge/Read-The%20Docs-blue"></a>
  </p>

</div>

---

**CogniCore** is a modern Python framework designed to streamline the development of sophisticated conversational AI agents. It provides the essential building blocks for creating agents with persistent memory, swappable LLM backends, and powerful tool-use capabilities.

What makes CogniCore unique is its built-in **behavioral simulation framework**, which allows you to rigorously test your agent's reasoning and decision-making processes, ensuring they are reliable and perform as expected.

## Key Features

-   🤖 **Modular & Extensible**: Swap out components like LLMs, memory, and tools with ease thanks to a clean, abstraction-based design.
-   🛠️ **Powerful Tool Integration**: Equip your agents with tools to interact with APIs, databases, or any other external service. The agent's LLM can reason about when and how to use them.
-   🧪 **Built-in Simulation Framework**: Go beyond unit tests. Write behavioral scenarios to validate your agent's complex conversational logic and tool-use chains.
-   🧠 **LLM Agnostic**: Ships with an `OpenAI_LLM` client but is designed to work with any Large Language Model through its `BaseLLM` abstraction.
-   💾 **Flexible Memory**: Includes a simple `VolatileMemory` for quick starts, with a clear interface for adding persistent memory backends (e.g., file or database storage).
-   ✨ **Modern & Tested**: Built with modern Python practices (like `uv` and `pyproject.toml`), fully type-hinted, and has a comprehensive test suite.

## Installation

CogniCore is available on PyPI and can be installed with your favorite package manager.

```bash
# Using uv (recommended)
uv pip install cognicore

# Or using standard pip
pip install cognicore
```

## Quick Start

Get your first agent running in just a few lines of code. Make sure your `OPENAI_API_KEY` environment variable is set.

```python
from cognicore import Agent, OpenAI_LLM, VolatileMemory, CalculatorTool

# 1. Assemble the agent's components
llm = OpenAI_LLM()
memory = VolatileMemory()
tools = [CalculatorTool()]

# 2. Create the agent with a system prompt
agent = Agent(
    llm=llm,
    memory=memory,
    tools=tools,
    system_prompt="You are Cogni, a helpful assistant with a calculator."
)

# 3. Start a conversation!
response = agent.chat("Hi there! What is 125 divided by 5?")
print(response)

# Expected output: "125 divided by 5 is 25.0."
```

## Documentation

For full details on all modules, how-to guides, and advanced usage, please see the **[Official Documentation](https://cognicore-ai.readthedocs.io/en/latest/)**.

The documentation covers:
-   Creating custom tools.
-   Writing and running behavioral simulations.
-   Adding new LLM backends.
-   Implementing persistent memory.
-   The complete API Reference.

## Contributing

Contributions are welcome! Whether it's reporting a bug, submitting a feature request, or writing code, we appreciate your help. Please see our contributing guidelines (you will need to create a `CONTRIBUTING.md` file for this) before getting started.

1.  Fork the repository.
2.  Create a new virtual environment and install the development dependencies:
    ```bash
    uv pip install -e ".[dev]"
    ```
3.  Set up the pre-commit hooks:
    ```bash
    pre-commit install
    ```
4.  Make your changes and ensure the tests pass:
    ```bash
    pytest
    ```
5.  Submit a pull request!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.