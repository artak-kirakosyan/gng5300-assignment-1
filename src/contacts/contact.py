"""
This module contains the definition of the Contact entry
"""
import datetime
import re
import uuid
from typing import Optional

from audit import get_logger_by_name
from exceptions.exceptions import InvalidPhoneNumberException, InvalidEmailException, InvalidNameException


class Contact:
    """
    This class is intended for storing a single contact and its arguments.
    The updated date of the class is automatically refreshed once a change is made to the class fields.
    This can be controlled by the property setters. just call the __refresh_updated_date method on any setter
    you want to keep track of
    """
    logger = get_logger_by_name("ContactLogger")
    _PHONE_NUMBER_PATTERN = re.compile(r"^\(\d{3}\) \d{3}-\d{4}$")
    _EMAIL_PATTERN = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$')

    _id: uuid.UUID
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
        self._id = uuid.uuid4()
        self.validate_phone_number(phone_number)
        self.validate_name(first_name)
        self.validate_name(last_name)
        self.validate_email(email)
        self._first_name = first_name
        self._last_name = last_name
        self._phone_number = phone_number
        self._email = email
        self._address = address
        self.__created_date = datetime.datetime.now()
        self.__refresh_updated_date()
        self.logger.info("Contact '%s'(id=%s) created", self.full_name, self.contact_id)

    def __refresh_updated_date(self):
        self.__updated_date = datetime.datetime.now()

    @property
    def contact_id(self) -> str:
        return str(self._id)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self.validate_name(value)
        self._first_name = value
        self.__refresh_updated_date()
        self.logger.info("First name of %s updated to %s", self.contact_id, self.first_name)

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        self.validate_name(value)
        self._last_name = value
        self.__refresh_updated_date()
        self.logger.info("Last name of %s updated to %s", self.contact_id, self.last_name)

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str):
        self.validate_phone_number(value)
        self._phone_number = value
        self.__refresh_updated_date()
        self.logger.info("Phone number of %s updated to %s", self.contact_id, self.phone_number)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value: Optional[str]):
        self.validate_email(value)
        self._email = value
        self.__refresh_updated_date()
        self.logger.info("Email of %s updated to %s", self.contact_id, self.email)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value: Optional[str]):
        self._address = value
        self.__refresh_updated_date()
        self.logger.info("Address of %s updated to %s", self.contact_id, self.address)

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
    def validate_name(cls, name: str):
        if name is None:
            raise InvalidNameException("Invalid name")

    @classmethod
    def create_contact_from_command_line(cls) -> 'Contact':
        first_name = cls.get_validated_first_name()
        last_name = cls.get_validated_last_name()
        phone_number = cls.get_validated_phone_number()
        email = cls.get_validated_email()
        address = cls.get_validated_address()
        contact = cls(first_name, last_name, phone_number, email, address)
        return contact

    @classmethod
    def get_validated_phone_number(cls):
        phone_number = input("Enter Phone Number(format: (###) ###-####): ")
        cls.validate_phone_number(phone_number)
        return phone_number

    @classmethod
    def get_validated_address(cls):
        address = input("Enter Address (optional): ")
        if address == "":
            address = None
        return address

    @classmethod
    def get_validated_email(cls):
        email = input("Enter Email (optional): ")
        if email == "":
            email = None
        cls.validate_email(email)
        return email

    @classmethod
    def get_validated_first_name(cls):
        first_name = input("Enter First Name: ")
        if first_name == "":
            first_name = None
        cls.validate_name(first_name)
        return first_name

    @classmethod
    def get_validated_last_name(cls):
        last_name = input("Enter Last Name: ")
        if last_name == "":
            last_name = None
        cls.validate_name(last_name)
        return last_name
