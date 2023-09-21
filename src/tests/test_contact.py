"""
Tests for Contact class
"""
import unittest
from datetime import datetime

from contacts.contact import Contact
from exceptions.exceptions import InvalidPhoneNumberException, InvalidEmailException


class TestContact(unittest.TestCase):
    """
    Basic unit tests for Contact class
    """

    def setUp(self):
        self.contact = Contact(
            first_name="John",
            last_name="Doe",
            phone_number="(123) 456-7890",
            email="john@example.com",
            address="123 Main St"
        )

    def test_initialization(self):
        self.assertEqual(self.contact.first_name, "John")
        self.assertEqual(self.contact.last_name, "Doe")
        self.assertEqual(self.contact.phone_number, "(123) 456-7890")
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
        self.contact.phone_number = "(987) 654-3210"
        self.assertEqual(self.contact.phone_number, "(987) 654-3210")
        self.assertGreater(self.contact.updated_date, self.contact.created_date)

    def test_update_email(self):
        self.contact.email = "jane@example.com"
        self.assertEqual(self.contact.email, "jane@example.com")
        self.assertGreater(self.contact.updated_date, self.contact.created_date)

    def test_update_address(self):
        self.contact.address = "456 Elm St"
        self.assertEqual(self.contact.address, "456 Elm St")
        self.assertGreater(self.contact.updated_date, self.contact.created_date)

    def test_contact_invalid_phone_number(self):
        invalid_phone_numbers = [
            "123-456-7890",  # Missing parentheses
            "(555) 1234567",  # Missing hyphen
            "(999) 00-12345",  # Extra digit in the last group
            "(555) 123-45678",  # Extra digit in the last group
            "(555) 12a-4567",  # Non-digit character
            "abc(123) 456-7890",  # Invalid format
        ]
        for phone_number in invalid_phone_numbers:
            with self.assertRaises(InvalidPhoneNumberException):
                Contact(
                    first_name="John",
                    last_name="Doe",
                    phone_number=phone_number,
                    email="john@example.com",
                    address="123 Main St"
                )


class TestPhoneNumberPattern(unittest.TestCase):
    def test_valid_phone_numbers(self):
        valid_phone_numbers = [
            "(123) 456-7890",
            "(555) 123-4567",
            "(999) 000-1234",
        ]

        for phone_number in valid_phone_numbers:
            with self.subTest(phone_number=phone_number):
                Contact.validate_phone_number(phone_number)

    def test_invalid_phone_numbers(self):
        invalid_phone_numbers = [
            "",  # empty string
            "123-456-7890",  # Missing parentheses
            "(555) 1234567",  # Missing hyphen
            "(999) 00-12345",  # Extra digit in the last group
            "(555) 123-45678",  # Extra digit in the last group
            "(555) 12a-4567",  # Non-digit character
            "abc(123) 456-7890",  # Invalid format
        ]

        for phone_number in invalid_phone_numbers:
            with self.subTest(phone_number=phone_number):
                with self.assertRaises(InvalidPhoneNumberException):
                    Contact.validate_phone_number(phone_number)


class TestEmailPattern(unittest.TestCase):
    def test_valid_emails(self):
        valid_emails = [
            "test@example.com",
            "user1234@subdomain.example.co.uk",
            "user.name@example-domain.com",
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                Contact.validate_email(email)

    def test_invalid_emails(self):
        invalid_emails = [
            "",  # empty string
            "invalid-email",  # Missing "@" and domain
            "user@invalid-domain",  # Invalid domain
            "@example.com",  # Missing local part
            "user@.com",  # Missing domain name
            "user@example.",  # Missing top-level domain
            "user@ex@mple.com",  # Invalid character in domain
            "user@example.com."  # Extra dot in top-level domain
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                with self.assertRaises(InvalidEmailException):
                    Contact.validate_email(email)
