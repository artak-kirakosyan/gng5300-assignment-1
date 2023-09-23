"""
This module contains the definition of the PhoneBook entry
"""
from typing import List

from audit import get_logger_by_name
from contacts.contact import Contact
from contacts.filter import ContactFilter
from exceptions.exceptions import ContactAlreadyExistsException, NoContactsMatchedException, \
    ContactIsNotRegisteredException


class PhoneBook:
    logger = get_logger_by_name("PhoneBookLogger")
    _contacts: List[Contact]
    _contact_filter: ContactFilter
    _current_results: List[Contact]

    def __init__(self, contacts: List[Contact] = None):
        if contacts is None:
            contacts = []
        self.contacts = contacts
        self.contact_filter = ContactFilter()
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

    @current_results.setter
    def current_results(self, value: List[Contact]):
        self._current_results = value

    @contacts.setter
    def contacts(self, value):
        self._contacts = value

    @contact_filter.setter
    def contact_filter(self, value):
        self._contact_filter = value

    def add_contact(self, contact: Contact):
        if len(self.retrieve_contacts_by_id(contact.id)) != 0:
            raise ContactAlreadyExistsException(f"Contact {contact.id} already exists")
        self.contacts.append(contact)
        self.refresh_current_results()
        self.logger.info("Contact '%s'(id=%s) created", contact.full_name, contact.id)

    def retrieve_contacts_by_name(self, name: str) -> List[Contact]:
        return [
            contact for contact in self.contacts if name.lower() in contact.full_name.lower()
        ]

    def retrieve_contact_by_phone(self, phone_number: str) -> List[Contact]:
        return [contact for contact in self.contacts if phone_number in contact.phone_number]

    def retrieve_contacts_by_id(self, contact_id: str) -> List[Contact]:
        contacts = [contact for contact in self.contacts if contact_id == contact.id]
        return contacts

    def delete_contact(self, contact: Contact):
        if contact not in self.contacts:
            raise ContactIsNotRegisteredException(f"Contact {contact.id} is not registered")
        self.contacts.remove(contact)
        self.logger.info("Contact '%s'(id=%s) deleted", contact.full_name, contact.id)

    def delete_contacts_by_id(self, contact_id: str):
        contacts = [contact for contact in self.contacts if contact_id == contact.id]
        if len(contacts) == 0:
            raise NoContactsMatchedException(f"No contacts matched id: {contact_id}")
        for contact in contacts:
            self.delete_contact(contact)
        self.refresh_current_results()

    def apply(self, contact_filter: ContactFilter) -> List[Contact]:
        self.contact_filter = contact_filter
        self.current_results = list(filter(
            lambda contact: contact.matches(self.contact_filter),
            self.contacts))
        self.current_results = self.sort_values(self.current_results, self.contact_filter)
        return self.current_results

    def refresh_current_results(self):
        self.apply(self.contact_filter)

    @staticmethod
    def sort_values(contacts: List[Contact], contact_filter: ContactFilter) -> List[Contact]:
        """Implement me"""
