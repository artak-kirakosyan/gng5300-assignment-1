import abc

from audit import get_logger_by_name
from contacts.contact import Contact
from contacts.contact_printer import ContactPrinter
from exceptions.exceptions import TerminateActionLoopException
from phone_book.phone_book import PhoneBook
from util.user_input import get_boolean_from_user


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
        contact = Contact.create_contact_from_command_line()
        phone_book.add_contact(contact)
        print(f"Contact '{contact.full_name}'(id={contact.id}) created")


class ExitAction(Action):
    name = "Exit"
    logger = get_logger_by_name("ExitLogger")

    def execute(self, phone_book: PhoneBook):
        raise TerminateActionLoopException()


class ShowContacts(Action):
    name = "Show Contacts"
    logger = get_logger_by_name("ShowLogger")

    def execute(self, phone_book: PhoneBook):
        if len(phone_book.contacts) == 0:
            print("No contacts")
            return
        printer = ContactPrinter()
        print(printer.get_headers())
        for contact in phone_book.contacts:
            print(printer.to_line(contact))


class DeleteContact(Action):
    name = "Delete Contact"
    logger = get_logger_by_name("DeleteLogger")

    def execute(self, phone_book: PhoneBook):
        contact_id = input("Enter the contact id to delete: ")
        contacts = phone_book.retrieve_contacts_by_id(contact_id)

        print(f"Found {len(contacts)} contacts by {contact_id}")
        phone_book.delete_contacts_by_id(contact_id)
        print(f"Contacts with id:{contact_id} successfully deleted")


class UpdateFilter(Action):
    name = "Update Filter"
    logger = get_logger_by_name("UpdateFilter")

    def execute(self, phone_book: PhoneBook):
        """Implement me"""


class DeleteCurrentResults(Action):
    name = "Delete Current Results"
    logger = get_logger_by_name("DeleteCurrentResults")

    def execute(self, phone_book: PhoneBook):
        """Show how many results are there currently, ask for confirmation and delete"""
        if len(phone_book.current_results) == 0:
            print("No contacts matching current filter")
            return
        ShowCurrentContacts().execute(phone_book)
        is_sure = get_boolean_from_user(
            "Are you sure you want to delete all these contacts? (Type 'Yes' or 'Y' to confirm): "
        )
        if not is_sure:
            print("Operation cancelled")
            return
        for contact in phone_book.current_results:
            phone_book.delete_contact(contact)
        print("Current contacts deleted")


class ShowCurrentContacts(Action):
    name = "Show Current Contacts"
    logger = get_logger_by_name("ShowCurrentContacts")

    def execute(self, phone_book: PhoneBook):
        printer = ContactPrinter()
        print("Current filter is:")
        print(phone_book.contact_filter)
        print(f"Current filter matches {len(phone_book.current_results)} contacts shown below")
        if len(phone_book.current_results) == 0:
            print("No contacts matching current filter")
            return
        print(printer.get_headers())
        for contact in phone_book.contacts:
            print(printer.to_line(contact))
