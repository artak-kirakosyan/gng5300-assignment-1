"""
This module contains the definition of the PhoneBook entry
"""
from collections import defaultdict
from typing import List, Dict, Callable

from audit import get_logger_by_name
from contacts.contact import Contact
from contacts.filter import ContactFilter, ContactSort
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

    @classmethod
    def from_file(cls, file_path: str) -> 'PhoneBook':
        contacts = Contact.bulk_create_contacts_from_csv(file_path)
        return cls(contacts)

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
        if len(self.retrieve_contacts_by_id(contact.contact_id)) != 0:
            raise ContactAlreadyExistsException(f"Contact {contact.contact_id} already exists")
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
            raise ContactIsNotRegisteredException(f"Contact {contact.contact_id} is not registered")
        self.contacts.remove(contact)
        self.logger.info("Contact '%s'(id=%s) deleted", contact.full_name, contact.contact_id)

    def delete_contacts_by_id(self, contact_id: str):
        contacts = [contact for contact in self.contacts if contact_id == contact.contact_id]
        if len(contacts) == 0:
            raise NoContactsMatchedException(f"No contacts matched id: {contact_id}")
        for contact in contacts:
            self.delete_contact(contact)
        self.refresh_current_results()

    def apply(self, contact_filter: ContactFilter) -> List[Contact]:
        self.contact_filter = contact_filter
        self.current_results = list(filter(
            lambda contact: ContactFilter.matches(contact, self.contact_filter),
            self.contacts))
        self.current_results = self.sort_values(self.current_results, self.contact_filter)
        return self.current_results

    def refresh_current_results(self):
        self.apply(self.contact_filter)

    @staticmethod
    def sort_values(contacts: List[Contact], contact_filter: 'ContactFilter') -> List[Contact]:
        if contact_filter is None:
            return contacts

        # Define a sorting key function based on the sort_field enum
        def sorting_key(one: 'Contact'):
            key_map = {
                ContactSort.ID: one.contact_id,
                ContactSort.FIRST_NAME: one.first_name,
                ContactSort.LAST_NAME: one.last_name,
                ContactSort.PHONE_NUMBER: one.phone_number,
                ContactSort.CREATED_DATE: one.created_date,
                ContactSort.UPDATED_DATE: one.updated_date
            }
            return key_map.get(contact_filter.sort_field, one.updated_date)

        # Sort the contacts based on the sorting key and the ascending flag
        sorted_contacts = sorted(contacts, key=sorting_key, reverse=not contact_filter.ascending)
        return sorted_contacts

    @classmethod
    def get_grouped_by(
            cls,
            contacts: List[Contact],
            key: Callable[[Contact], str]
    ) -> Dict[str, List[Contact]]:
        groups = defaultdict(list)
        for contact in contacts:
            contact_key = key(contact)
            groups[contact_key].append(contact)
        return groups
