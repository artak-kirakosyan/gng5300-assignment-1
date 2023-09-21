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

        self.assertIn("1 - Create Contract", output)
        self.assertIn("2 - Exit", output)

    @patch("builtins.input", side_effect=["2"])
    def test_run_exit_action(self, mock_input):
        phone_book_controller = PhoneBookController()
        phone_book_controller.run()
