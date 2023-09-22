import datetime
from enum import Enum, auto
from typing import Optional


class ContactSort(Enum):
    ID = auto
    FIRST_NAME = auto
    LAST_NAME = auto
    PHONE_NUMBER = auto


class ContactFilter:
    search_query: Optional[str] = None

    min_created_date: Optional[datetime.datetime] = None
    max_created_date: Optional[datetime.datetime] = None

    min_updated_date: Optional[datetime.datetime] = None
    max_updated_date: Optional[datetime.datetime] = None
    ascending: bool = True
    sort_field: ContactSort = ContactSort.FIRST_NAME  # TODO implement null-first null-last
