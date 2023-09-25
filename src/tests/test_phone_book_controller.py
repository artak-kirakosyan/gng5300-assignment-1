import unittest
from io import StringIO
from unittest.mock import patch

from phone_book.phone_book_controller import PhoneBookController


class TestPhoneBookController(unittest.TestCase):
    def test_show_actions(self):
        phone_book_controller = PhoneBookController()
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            phone_book_controller.show_actions()
            output = mock_stdout.getvalue()

        self.assertIn("1 - Show Contacts", output)
        self.assertIn("2 - Create Contact", output)
        self.assertIn("3 - Edit Contact", output)
        self.assertIn("4 - Delete Contact", output)
        self.assertIn("5 - Group By Last Name First Letter", output)
        self.assertIn("6 - Group Current Contacts By Last Name First Letter", output)
        self.assertIn("7 - Delete Current Results", output)
        self.assertIn("8 - Show Current Contacts", output)
        self.assertIn("9 - Update Filter", output)
        self.assertIn("10 - Reset Filter", output)
        self.assertIn("11 - Import From File", output)
        self.assertIn("12 - Exit", output)

    @patch("builtins.input", side_effect=["12"])
    def test_run_exit_action(self, mock_input=None):
        assert mock_input
        phone_book_controller = PhoneBookController()
        phone_book_controller.run()
