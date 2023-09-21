"""
This module contains the definition of the PhoneBook entry
"""
from typing import List

from contacts.contact import Contact


class PhoneBook:
    _contacts: List[Contact]

    def __init__(self):
        self._contacts = []

    @property
    def contacts(self):
        return self._contacts

    def add_contact(self, contact: Contact):
        self.contacts.append(contact)

    def retrieve_contacts_by_name(self, name: str) -> List[Contact]:
        return [
            contact for contact in self.contacts if name.lower() in contact.full_name.lower()
        ]

    def retrieve_contact_by_phone(self, phone_number: str) -> List[Contact]:
        return [contact for contact in self.contacts if phone_number in contact.phone_number]

    def delete_contact(self, contact: Contact):
        self.contacts.remove(contact)
