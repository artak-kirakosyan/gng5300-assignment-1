import datetime
from typing import Optional


class Contact:
    def __init__(
            self,
            first_name: str,
            last_name: str,
            phone_number: str,
            email: Optional[str] = None,
            address: Optional[str] = None
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
