import datetime
from copy import copy
from enum import Enum, auto
from typing import Optional, Callable, List

from contacts.contact import Contact
from exceptions.exceptions import InvalidInputException
from util.user_input import get_boolean_from_user, get_datetime_from_user


class ContactSort(Enum):
    ID = auto()
    FIRST_NAME = auto()
    LAST_NAME = auto()
    PHONE_NUMBER = auto()
    CREATED_DATE = auto()
    UPDATED_DATE = auto()

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
    def get_updated_filter_from_command_line(cls, old: 'ContactFilter'):
        new_filter = copy(old)
        new_filter = cls.update_search_query(new_filter)
        new_filter = cls.update_min_created_date(new_filter)
        new_filter = cls.update_max_created_date(new_filter)
        new_filter = cls.update_min_updated_date(new_filter)
        new_filter = cls.update_max_updated_date(new_filter)
        new_filter = cls.update_sort_ascending(new_filter)
        new_filter = cls.update_sort_field(new_filter)
        return new_filter

    @classmethod
    def update_search_query(cls, old: 'ContactFilter') -> 'ContactFilter':
        print(f"Current value of 'Search Query' is {old.search_query}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = input("Type in the new search query(type query components separated by a space): ")
            if new_value == "":
                new_value = None
            old.search_query = new_value
        return old

    @classmethod
    def update_min_created_date(cls, old: 'ContactFilter') -> 'ContactFilter':
        print(f"Current value of 'Min Created Date' is {old.min_created_date}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = get_datetime_from_user("Type in the date: ")
            old.min_created_date = new_value
        return old

    @classmethod
    def update_max_created_date(cls, old: 'ContactFilter') -> 'ContactFilter':
        print(f"Current value of 'Max Created Date' is {old.max_created_date}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = get_datetime_from_user("Type in the date: ")
            old.max_created_date = new_value
        return old

    @classmethod
    def update_min_updated_date(cls, old: 'ContactFilter') -> 'ContactFilter':
        print(f"Current value of 'Min Updated Date' is {old.min_updated_date}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = get_datetime_from_user("Type in the date: ")
            old.min_updated_date = new_value
        return old

    @classmethod
    def update_max_updated_date(cls, old: 'ContactFilter') -> 'ContactFilter':
        print(f"Current value of 'Max Updated Date' is {old.max_updated_date}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = get_datetime_from_user("Type in the date: ")
            old.max_updated_date = new_value
        return old

    @classmethod
    def update_sort_ascending(cls, old: 'ContactFilter') -> 'ContactFilter':
        print(f"Current value of 'Is Sort Ascending' is {old.ascending}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = get_boolean_from_user("Do you want to keep the sort ascending?(Type 'Yes' or 'No':")
            old.ascending = new_value
        return old

    @classmethod
    def update_sort_field(cls, old: 'ContactFilter') -> 'ContactFilter':
        print(f"Current value of 'Sort Field' is {old.sort_field}")
        should_update = get_boolean_from_user()
        if should_update:
            choice = input(f"Select a sort field(should be one of {[e.name for e in ContactSort]}): ")
            try:
                new_value = ContactSort[choice]
            except KeyError as error:
                raise InvalidInputException("Invalid sort field") from error
            old.sort_field = new_value
        return old

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
        if value is None:
            return False
        if search_query is None:
            return True
        if " " in search_query:
            queries = search_query.split(" ")
        else:
            queries = [search_query]
        return any(query.lower() in value.lower() for query in queries)
