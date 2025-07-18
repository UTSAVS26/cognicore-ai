"""
CogniCore: A modular framework for building conversational AI agents.

This top-level package provides easy access to the most important classes
and components of the framework. By importing them here, users can enjoy
a cleaner and more convenient API.

Example:
    from cognicore import Agent, VolatileMemory, Tool

Attributes:
    __version__ (str): The current version of the CogniCore library.
"""

# Define the package version. This is a standard practice that allows users
# to check the version of the library they have installed.
__version__ = "0.1.0"

# Import key components from the submodules to make them directly accessible
# from the top-level 'cognicore' package.

# From the memory module
# From the agents module
from .agents import Agent

# From the new LLM module
from .llms import BaseLLM, LLMResponse, OpenAI_LLM, ToolCall
from .memory import BaseMemory, Message, VolatileMemory

# Simulation and Evaluation components
from .simulation import (
    Assertion,
    ResponseContainsAssertion,
    Scenario,
    SimulationResult,
    Simulator,
    ToolUsedAssertion,
)

# From the tools module
from .tools import CalculatorTool, Tool

# Use __all__ to explicitly define the public API of the package.
# This tells tools like linters and IDEs which names are meant to be
# imported from the package.
__all__ = [
    "__version__",
    # Agent
    "Agent",
    # LLMs
    "BaseLLM",
    "OpenAI_LLM",
    "LLMResponse",
    "ToolCall",
    # Memory
    "BaseMemory",
    "VolatileMemory",
    "Message",
    # Tools
    "Tool",
    "CalculatorTool",
    # Simulation
    "Simulator",
    "Scenario",
    "Assertion",
    "ToolUsedAssertion",
    "ResponseContainsAssertion",
    "SimulationResult",
]
