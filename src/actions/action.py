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
        contact = Contact.create_contract_from_command_line()
        phone_book.add_contact(contact)


class ExitAction(Action):
    name = "Exit"

    def execute(self, phone_book: PhoneBook):
        raise TerminateActionLoopException()
