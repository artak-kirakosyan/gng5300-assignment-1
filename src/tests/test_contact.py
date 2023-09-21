"""
Tests for Contact class
"""
import unittest
from datetime import datetime

from contacts.contact import Contact


class TestContact(unittest.TestCase):
    """
    Basic unit tests for Contact class
    """

    def setUp(self):
        self.contact = Contact(
            first_name="John",
            last_name="Doe",
            phone_number="123-456-7890",
            email="john@example.com",
            address="123 Main St"
        )

    def test_initialization(self):
        self.assertEqual(self.contact.first_name, "John")
        self.assertEqual(self.contact.last_name, "Doe")
        self.assertEqual(self.contact.phone_number, "123-456-7890")
        self.assertEqual(self.contact.email, "john@example.com")
        self.assertEqual(self.contact.address, "123 Main St")
        self.assertIsInstance(self.contact.created_date, datetime)
        self.assertIsInstance(self.contact.updated_date, datetime)

    def test_update_first_name(self):
        self.contact.first_name = "Jane"
        self.assertEqual(self.contact.first_name, "Jane")
        self.assertGreater(self.contact.updated_date, self.contact.created_date)

    def test_update_last_name(self):
        self.contact.last_name = "Smith"
        self.assertEqual(self.contact.last_name, "Smith")
        self.assertGreater(self.contact.updated_date, self.contact.created_date)

    def test_update_phone_number(self):
        self.contact.phone_number = "987-654-3210"
        self.assertEqual(self.contact.phone_number, "987-654-3210")
        self.assertGreater(self.contact.updated_date, self.contact.created_date)

    def test_update_email(self):
        self.contact.email = "jane@example.com"
        self.assertEqual(self.contact.email, "jane@example.com")
        self.assertGreater(self.contact.updated_date, self.contact.created_date)

    def test_update_address(self):
        self.contact.address = "456 Elm St"
        self.assertEqual(self.contact.address, "456 Elm St")
        self.assertGreater(self.contact.updated_date, self.contact.created_date)
