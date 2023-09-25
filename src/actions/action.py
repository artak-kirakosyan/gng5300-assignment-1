import abc

from contacts.contact import Contact
from contacts.contact_editor import ContactEditor
from contacts.contact_printer import ContactPrinter
from contacts.filter import ContactFilter
from exceptions.exceptions import TerminateActionLoopException
from phone_book.phone_book import PhoneBook
from util.grouping import group_and_print
from util.user_input import get_boolean_from_user


class Action(abc.ABC):
    name: str

    @abc.abstractmethod
    def execute(self, phone_book: PhoneBook):
        """This abstract method should be implemented by specific actions"""

    @property
    @abc.abstractmethod
    def name(self):
        """This name is used to show the action to the user"""


class ContactCreateAction(Action):
    name = "Create Contact"

    def execute(self, phone_book: PhoneBook):
        contact = Contact.create_contact_from_command_line()
        phone_book.add_contact(contact)
        print(f"Contact '{contact.full_name}'(id={contact.contact_id}) created")


class ExitAction(Action):
    name = "Exit"

    def execute(self, phone_book: PhoneBook):
        raise TerminateActionLoopException()


class ShowContacts(Action):
    name = "Show Contacts"

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

    def execute(self, phone_book: PhoneBook):
        contact_id = input("Enter the contact id to delete: ")
        contacts = phone_book.retrieve_contacts_by_id(contact_id)

        print(f"Found {len(contacts)} contacts by {contact_id}")
        phone_book.delete_contacts_by_id(contact_id)
        print(f"Contacts with id:{contact_id} successfully deleted")


class UpdateFilter(Action):
    name = "Update Filter"

    def execute(self, phone_book: PhoneBook):
        old_filter = phone_book.contact_filter
        updated_filter = ContactFilter.get_updated_filter_from_command_line(old_filter)
        phone_book.apply(updated_filter)
        ShowCurrentContacts().execute(phone_book)


class DeleteCurrentResults(Action):
    name = "Delete Current Results"

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

    def execute(self, phone_book: PhoneBook):
        print("Current filter is:")
        print(phone_book.contact_filter)
        print(f"Current filter matches {len(phone_book.current_results)} contacts shown below")
        printer = ContactPrinter()
        printer.print_contacts(phone_book.current_results)


class ResetFilter(Action):
    name = "Reset Filter"

    def execute(self, phone_book: PhoneBook):
        new_filter = ContactFilter()
        phone_book.apply(new_filter)
        print("Filter is reset")
        ShowCurrentContacts().execute(phone_book)


class EditContact(Action):
    name = "Edit Contact"

    def execute(self, phone_book: PhoneBook):
        contact_id = input("Enter the contact id to delete: ")
        contacts = phone_book.retrieve_contacts_by_id(contact_id)

        if len(contacts) == 0:
            print("No contact found, can't edit")
            return
        if len(contacts) > 1:
            print(f"Too many contacts matched {contact_id}, delete them to make a unique selection")
            return
        contact = contacts[0]
        ContactEditor.update_from_command_line(contact)
        print(f"Contact {contact.contact_id} updated")


class GroupByLastNameFirstLetter(Action):
    name = "Group By Last Name First Letter"

    def execute(self, phone_book: PhoneBook):
        contacts = phone_book.contacts
        group_and_print(contacts, lambda contact: contact.last_name[0])


class GroupCurrentContactsByLastNameFirstLetter(Action):
    name = "Group Current Contacts By Last Name First Letter"

    def execute(self, phone_book: PhoneBook):
        contacts = phone_book.current_results
        group_and_print(contacts, lambda contact: contact.last_name[0])


class ImportFromFile(Action):
    name = "Import From File"

    def execute(self, phone_book: PhoneBook):
        file_path = input("Insert the full path to the CSV file: ")
        contacts = Contact.bulk_create_contacts_from_csv(file_path)
        print(f"Imported {len(contacts)} contacts")
        for contact in contacts:
            phone_book.add_contact(contact)
        print(f"All {len(contacts)} contacts have been saved")
