"""
Unit tests for the memory module.

These tests validate the functionality of the BaseMemory implementations,
ensuring that they correctly store, retrieve, and manage conversation history.
"""

import unittest

from cognicoreai import Message, VolatileMemory


class TestVolatileMemory(unittest.TestCase):
    """Test suite for the VolatileMemory class."""

    def setUp(self):
        """
        This method is called before each test function is executed.
        It sets up a fresh VolatileMemory instance for each test.
        """
        self.memory = VolatileMemory()

    def test_initialization(self):
        """Test that memory is initialized with an empty history."""
        self.assertEqual(self.memory.get_history(), [])

    def test_add_message(self):
        """Test that a single message can be added correctly."""
        message: Message = {"role": "user", "content": "Hello, world!"}
        self.memory.add_message(message)
        self.assertEqual(len(self.memory.get_history()), 1)
        self.assertEqual(self.memory.get_history()[0], message)

    def test_get_history_returns_copy(self):
        """
        Test that get_history() returns a copy, not a reference, to prevent
        accidental external modification of the memory state.
        """
        message: Message = {"role": "user", "content": "Hello!"}
        self.memory.add_message(message)

        history_copy = self.memory.get_history()
        self.assertEqual(len(history_copy), 1)

        # Modify the returned copy
        history_copy.append({"role": "assistant", "content": "Modified!"})

        # The original memory should remain unchanged
        self.assertEqual(len(self.memory.get_history()), 1)
        self.assertEqual(self.memory.get_history()[0], message)

    def test_clear(self):
        """Test that the clear method removes all messages."""
        messages: list[Message] = [
            {"role": "user", "content": "First message."},
            {"role": "assistant", "content": "Second message."},
        ]
        for msg in messages:
            self.memory.add_message(msg)

        self.assertEqual(len(self.memory.get_history()), 2)

        self.memory.clear()
        self.assertEqual(self.memory.get_history(), [])
