"""
This module contains the definition of the Contact entry
"""
import datetime
import re
from typing import Optional

from exceptions.exceptions import InvalidPhoneNumberException, InvalidEmailException


class Contact:
    """
    This class is intended for storing a single contact and its arguments.
    The updated date of the class is automatically refreshed once a change is made to the class fields.
    This can be controlled by the property setters. just call the __refresh_updated_date method on any setter
    you want to keep track of
    """
    _PHONE_NUMBER_PATTERN = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
    _EMAIL_PATTERN = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$')

    _first_name: str
    _last_name: str
    _phone_number: str
    _email: Optional[str]
    _address: Optional[str]
    __created_date: datetime
    __updated_date: datetime

    def __init__(
            self,
            first_name: str,
            last_name: str,
            phone_number: str,
            email: Optional[str] = None,
            address: Optional[str] = None
    ):
        self.validate_phone_number(phone_number)
        self.validate_email(email)
        self._first_name = first_name
        self._last_name = last_name
        self._phone_number = phone_number
        self._email = email
        self._address = address
        self.__created_date = datetime.datetime.now()
        self.__refresh_updated_date()

    def __refresh_updated_date(self):
        self.__updated_date = datetime.datetime.now()

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._first_name = value
        self.__refresh_updated_date()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        self._last_name = value
        self.__refresh_updated_date()

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str):
        self._phone_number = value
        self.__refresh_updated_date()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value: Optional[str]):
        self._email = value
        self.__refresh_updated_date()

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value: Optional[str]):
        self._address = value
        self.__refresh_updated_date()

    @property
    def created_date(self):
        return self.__created_date

    @property
    def updated_date(self):
        return self.__updated_date

    @property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name

    @classmethod
    def validate_phone_number(cls, phone_number: str):
        if phone_number is None:
            raise InvalidPhoneNumberException("Phone number is required")
        if cls._PHONE_NUMBER_PATTERN.match(phone_number) is None:
            raise InvalidPhoneNumberException("Phone number should be of the form (###) ###-####")

    @classmethod
    def validate_email(cls, email: str):
        if email is None:
            return
        if cls._EMAIL_PATTERN.match(email) is None:
            raise InvalidEmailException("Invalid email")

    @classmethod
    def create_contract_from_command_line(cls) -> 'Contact':
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        phone_number = input("Enter Phone Number: ")
        cls.validate_phone_number(phone_number)
        email = input("Enter Email (optional): ")
        address = input("Enter Address (optional): ")

        contact = cls(first_name, last_name, phone_number, email, address)
        return contact
