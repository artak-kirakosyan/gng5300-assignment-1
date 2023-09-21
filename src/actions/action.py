import abc

from contacts.contact import Contact
from exceptions.exceptions import TerminateActionLoopException
from phone_book.phone_book import PhoneBook


class Action(abc.ABC):
    name: str

    @abc.abstractmethod
    def execute(self, phone_book: PhoneBook):
        """This abstract method should be implemented by specific actions"""

    @property
    @abc.abstractmethod
    def name(self):
        """Implement me"""


class ContactCreateAction(Action):
    name = "Create Contract"

    def execute(self, phone_book: PhoneBook):
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        phone_number = input("Enter Phone Number: ")
        email = input("Enter Email (optional): ")
        address = input("Enter Address (optional): ")

        contact = Contact(first_name, last_name, phone_number, email, address)
        phone_book.add_contact(contact)


class ExitAction(Action):
    name = "Exit"

    def execute(self, phone_book: PhoneBook):
        raise TerminateActionLoopException()
