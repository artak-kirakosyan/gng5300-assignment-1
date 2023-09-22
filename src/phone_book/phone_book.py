"""
This module contains the definition of the PhoneBook entry
"""
from typing import List, Optional

from audit import get_logger_by_name
from contacts.contact import Contact
from contacts.filter import ContactFilter
from exceptions.exceptions import ContactAlreadyExists, NoContactsMatched, ContactIsNotRegistered


class PhoneBook:
    logger = get_logger_by_name("PhoneBookLogger")
    _contacts: List[Contact]
    _contact_filter: Optional[ContactFilter]
    _current_results: List[Contact]

    def __init__(self, contacts: List[Contact] = None):
        if contacts is None:
            contacts = []
        self._contacts = contacts
        self._contact_filter: Optional[ContactFilter] = ContactFilter()
        self.refresh_current_results()

    @property
    def contacts(self):
        return self._contacts

    @property
    def current_results(self):
        return self._current_results

    @property
    def contact_filter(self):
        return self._contact_filter

    def add_contact(self, contact: Contact):
        if len(self.retrieve_contacts_by_id(contact.contact_id)) != 0:
            raise ContactAlreadyExists(f"Contact {contact.contact_id} already exists")
        self.contacts.append(contact)
        self.refresh_current_results()
        self.logger.info("Contact '%s'(id=%s) created", contact.full_name, contact.contact_id)

    def retrieve_contacts_by_name(self, name: str) -> List[Contact]:
        return [
            contact for contact in self.contacts if name.lower() in contact.full_name.lower()
        ]

    def retrieve_contact_by_phone(self, phone_number: str) -> List[Contact]:
        return [contact for contact in self.contacts if phone_number in contact.phone_number]

    def retrieve_contacts_by_id(self, contact_id: str) -> List[Contact]:
        contacts = [contact for contact in self.contacts if contact_id == contact.contact_id]
        return contacts

    def delete_contact(self, contact: Contact):
        if contact not in self.contacts:
            raise ContactIsNotRegistered(f"Contact {contact.contact_id} is not registered")
        self.contacts.remove(contact)
        self.logger.info("Contact '%s'(id=%s) deleted", contact.full_name, contact.contact_id)

    def delete_contacts_by_id(self, contact_id: str):
        contacts = [contact for contact in self.contacts if contact_id == contact.contact_id]
        if len(contacts) == 0:
            raise NoContactsMatched(f"No contacts matched id: {contact_id}")
        for contact in contacts:
            self.delete_contact(contact)
        self.refresh_current_results()

    def apply(self, contact_filter: ContactFilter) -> List[Contact]:
        self._contact_filter = contact_filter
        self._current_results = list(filter(
            lambda contact: contact.matches(self._contact_filter),
            self.contacts))
        # TODO implement sort
        return self._current_results

    def refresh_current_results(self):
        self.apply(self.contact_filter)
