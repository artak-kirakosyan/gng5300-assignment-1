import datetime
from enum import Enum, auto
from typing import Optional


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
        filter_str = f"Filter:\n"
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
