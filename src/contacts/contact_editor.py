from contacts.contact import Contact
from util.user_input import get_boolean_from_user


class ContactEditor:
    @classmethod
    def update_from_command_line(cls, contact: Contact) -> Contact:
        contact = cls.update_first_name(contact)
        contact = cls.update_last_name(contact)
        contact = cls.update_phone_number(contact)
        contact = cls.update_email(contact)
        contact = cls.update_address(contact)
        return contact

    @classmethod
    def update_first_name(cls, contact: Contact) -> Contact:
        print(f"Current value of 'First Name' is {contact.first_name}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = Contact.get_validated_first_name()
            contact.first_name = new_value
        return contact

    @classmethod
    def update_last_name(cls, contact: Contact) -> Contact:
        print(f"Current value of 'Last Name' is {contact.last_name}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = Contact.get_validated_last_name()
            contact.last_name = new_value
        return contact

    @classmethod
    def update_phone_number(cls, contact: Contact) -> Contact:
        print(f"Current value of 'Phone Number' is {contact.phone_number}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = Contact.get_validated_phone_number()
            contact.phone_number = new_value
        return contact

    @classmethod
    def update_email(cls, contact: Contact) -> Contact:
        print(f"Current value of 'Email' is {contact.email}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = Contact.get_validated_email()
            contact.email = new_value
        return contact

    @classmethod
    def update_address(cls, contact: Contact) -> Contact:
        print(f"Current value of 'Address' is {contact.address}")
        should_update = get_boolean_from_user()
        if should_update:
            new_value = Contact.get_validated_address()
            contact.address = new_value
        return contact
