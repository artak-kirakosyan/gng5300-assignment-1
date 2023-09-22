import abc

from audit import get_logger_by_name
from contacts.contact_printer import ContactPrinter
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
    name = "Create Contact"
    logger = get_logger_by_name("ContactCreateLogger")

    def execute(self, phone_book: PhoneBook):
        contact = Contact.create_contract_from_command_line()
        phone_book.add_contact(contact)


class ExitAction(Action):
    name = "Exit"
    logger = get_logger_by_name("ExitLogger")

    def execute(self, phone_book: PhoneBook):
        raise TerminateActionLoopException()


class ShowContacts(Action):
    name = "Show Contacts"
    logger = get_logger_by_name("ExitLogger")

    def execute(self, phone_book: PhoneBook):
        printer = ContactPrinter()
        if (len(phone_book.contacts)) == 0:
            print("No contacts")
            return
        print(printer.get_headers())
        for contact in phone_book.contacts:
            print(printer.to_line(contact))
