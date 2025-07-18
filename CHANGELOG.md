# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-18

This is the initial public release of CogniCoreAI.

### Added
- Core `Agent` class for orchestrating conversations.
- `BaseLLM` abstraction layer with an `OpenAI_LLM` implementation.
- `BaseMemory` abstraction with a `VolatileMemory` implementation.
- `Tool` abstraction and a built-in `CalculatorTool`.
- `Simulator` framework for running behavioral tests on agents.
- `Scenario` and `Assertion` classes (`ToolUsedAssertion`, `ResponseContainsAssertion`) for defining test cases.
- Comprehensive test suite for all modules.
- Full documentation site built with Sphinx and the Furo theme.
- Ruff and Pytest configured for code quality and testing.
- Project structure configured with `pyproject.toml` for modern packaging.