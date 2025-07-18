"""
Unit tests for the tools module.

These tests ensure that all tools behave as expected, correctly parsing
their inputs and returning the correct outputs.
"""

import unittest

from cognicoreai import CalculatorTool


class TestCalculatorTool(unittest.TestCase):
    """Test suite for the CalculatorTool."""

    def setUp(self):
        """Set up a fresh CalculatorTool instance for each test."""
        self.calculator = CalculatorTool()

    def test_addition(self):
        """Test correct addition."""
        self.assertEqual(self.calculator.run("2 + 3"), "5.0")
        self.assertEqual(self.calculator.run("10.5 + 5"), "15.5")

    def test_subtraction(self):
        """Test correct subtraction."""
        self.assertEqual(self.calculator.run("10 - 4"), "6.0")

    def test_multiplication(self):
        """Test correct multiplication."""
        self.assertEqual(self.calculator.run("5 * 5"), "25.0")

    def test_division(self):
        """Test correct division."""
        self.assertEqual(self.calculator.run("20 / 4"), "5.0")

    def test_invalid_operator(self):
        """Test that an unsupported operator returns an error."""
        response = self.calculator.run("5 ^ 2")
        self.assertIn("Error: Invalid operator", response)

    def test_invalid_input_format(self):
        """Test that malformed input returns an error."""
        response = self.calculator.run("five plus three")
        self.assertIn("Error: Invalid input format", response)

    def test_not_enough_arguments(self):
        """Test that input with missing parts returns an error."""
        response = self.calculator.run("5 +")
        self.assertIn("Error: Invalid input format", response)
