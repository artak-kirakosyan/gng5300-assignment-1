from typing import List, Callable

from contacts.contact import Contact
from contacts.contact_printer import ContactPrinter
from phone_book.phone_book import PhoneBook


def group_and_print(contacts: List[Contact], key: Callable[[Contact], str]):
    if len(contacts) == 0:
        print("No contacts, can't group")
        return
    groups = PhoneBook.get_grouped_by(contacts, key)
    printer = ContactPrinter()
    for name, group in groups.items():
        print(f"Group Name: {name}")
        print('-' * 20)
        printer.print_contacts(group)
