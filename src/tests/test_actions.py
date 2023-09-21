import unittest
from unittest.mock import patch

from actions.action import ContactCreateAction, ExitAction
from exceptions.exceptions import TerminateActionLoopException
from phone_book.phone_book import PhoneBook


class TestAction(unittest.TestCase):
    def test_contact_create_action(self):
        phone_book = PhoneBook()
        action = ContactCreateAction()
        with patch("builtins.input", side_effect=["John", "Doe", "(123) 456-7890", None, ""]):
            action.execute(phone_book)
        self.assertEqual(len(phone_book.contacts), 1)

    def test_exit_action(self):
        action = ExitAction()
        with self.assertRaises(TerminateActionLoopException):
            action.execute(PhoneBook())
