import unittest

from contacts.contact import Contact
from phone_book.phone_book import PhoneBook


class TestPhoneBook(unittest.TestCase):
    def test_add_contact(self):
        phone_book = PhoneBook()
        contact = Contact("John", "Doe", "(123) 456-7890")
        phone_book.add_contact(contact)
        self.assertEqual(len(phone_book.contacts), 1)

    def test_retrieve_contacts_by_name(self):
        phone_book = PhoneBook()
        contact1 = Contact("John", "Doe", "(123) 456-7890")
        contact2 = Contact("Alice", "Smith", "(987) 654-3210")
        phone_book.add_contact(contact1)
        phone_book.add_contact(contact2)

        retrieved_contacts = phone_book.retrieve_contacts_by_name("John Doe")
        self.assertEqual(len(retrieved_contacts), 1)
        self.assertEqual(retrieved_contacts[0], contact1)

    def test_retrieve_contact_by_phone(self):
        phone_book = PhoneBook()
        contact1 = Contact("John", "Doe", "(123) 456-7890")
        contact2 = Contact("Alice", "Smith", "(987) 654-3210")
        phone_book.add_contact(contact1)
        phone_book.add_contact(contact2)
        retrieved_contacts = phone_book.retrieve_contact_by_phone("(987) 654-3210")
        self.assertEqual(len(retrieved_contacts), 1)
        self.assertEqual(retrieved_contacts[0], contact2)

    def test_delete_contact(self):
        phone_book = PhoneBook()
        contact = Contact("John", "Doe", "(123) 456-7890")
        phone_book.add_contact(contact)
        phone_book.delete_contact(contact)
        self.assertEqual(len(phone_book.contacts), 0)
