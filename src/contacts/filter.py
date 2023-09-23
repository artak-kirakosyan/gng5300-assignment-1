import datetime
from enum import Enum, auto
from typing import Optional, Callable, List

from contacts.contact import Contact


class ContactSort(Enum):
    ID = auto
    FIRST_NAME = auto
    LAST_NAME = auto
    PHONE_NUMBER = auto
    CREATED_DATE = auto
    UPDATED_DATE = auto

    def __str__(self):
        return self.name


class ContactFilter:
    search_query: Optional[str] = None

    min_created_date: Optional[datetime.datetime] = None
    max_created_date: Optional[datetime.datetime] = None

    min_updated_date: Optional[datetime.datetime] = None
    max_updated_date: Optional[datetime.datetime] = None

    ascending: bool = True
    sort_field: ContactSort = ContactSort.UPDATED_DATE

    def __str__(self):
        filter_str = "Filter:\n"
        filter_str += f"  Search Query: {self.search_query}\n"
        filter_str += f"  Min Created Date: {self.min_created_date}\n"
        filter_str += f"  Max Created Date: {self.max_created_date}\n"
        filter_str += f"  Min Updated Date: {self.min_updated_date}\n"
        filter_str += f"  Max Updated Date: {self.max_updated_date}\n"
        filter_str += f"  Ascending: {self.ascending}\n"
        filter_str += f"  Sort Field: {self.sort_field}\n"
        return filter_str

    @classmethod
    def from_command_line(cls):
        """Implement me"""

    @classmethod
    def matches(cls, contact: Contact, contact_filter: 'ContactFilter'):
        criteria: List[Callable[[Contact, 'ContactFilter'], bool]] = [
            cls.is_matching_max_created_date,
            cls.is_matching_min_created_date,
            cls.is_matching_max_updated_date,
            cls.is_matching_min_updated_date,
            cls.is_matching_search_query

        ]
        for criterion in criteria:
            if not criterion(contact, contact_filter):
                return False
        return True

    @classmethod
    def is_matching_max_created_date(cls, contact: Contact, contact_filter: 'ContactFilter') -> bool:
        if contact_filter.max_created_date is not None:
            if contact.created_date > contact_filter.max_created_date:
                return False
        return True

    @classmethod
    def is_matching_min_created_date(cls, contact: Contact, contact_filter: 'ContactFilter') -> bool:
        if contact_filter.min_created_date is not None:
            if contact.created_date < contact_filter.min_created_date:
                return False
        return True

    @classmethod
    def is_matching_max_updated_date(cls, contact: Contact, contact_filter: 'ContactFilter') -> bool:
        if contact_filter.max_updated_date is not None:
            if contact.updated_date > contact_filter.max_updated_date:
                return False
        return True

    @classmethod
    def is_matching_min_updated_date(cls, contact: Contact, contact_filter: 'ContactFilter') -> bool:
        if contact_filter.min_updated_date is not None:
            if contact.updated_date < contact_filter.min_updated_date:
                return False
        return True

    @classmethod
    def is_matching_search_query(cls, contact: Contact, contact_filter: 'ContactFilter') -> bool:
        if contact_filter.search_query is not None:
            values_to_match = [contact.first_name, contact.last_name, contact.phone_number, contact.email,
                               contact.address]
            match_results = [
                cls.is_value_matching_query(contact_filter.search_query, value) for value in values_to_match
            ]
            if any(match_results):
                return True
            return False
        return True

    @classmethod
    def is_value_matching_query(cls, search_query: str, value: str) -> bool:
        """Implement me"""
