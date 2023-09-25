import datetime
import unittest

from contacts.contact import Contact
from contacts.filter import ContactFilter


class TestContactFilter(unittest.TestCase):
    def setUp(self):
        self.john: Contact = Contact("John", "Doe", "(123) 456-7890", "john@example.com", "123 Main St")
        self.jane: Contact = Contact("Jane", "Smith", "(987) 654-3210", "jane@example.com", "456 Elm St")
        self.before_joe_created = datetime.datetime.now()
        self.joe: Contact = Contact("Joe", "Smith", "(987) 654-3210", "joe@uottawa.ca", "789 Last St")

    def test_is_matching_max_created_date(self):
        contact_filter = ContactFilter()
        contact_filter.max_created_date = self.before_joe_created

        self.assertTrue(contact_filter.is_matching_max_created_date(self.john, contact_filter))
        self.assertTrue(contact_filter.is_matching_max_created_date(self.jane, contact_filter))

        self.assertTrue(contact_filter.is_matching_max_created_date(self.john, contact_filter))
        self.assertTrue(contact_filter.is_matching_max_created_date(self.jane, contact_filter))
        self.assertFalse(contact_filter.is_matching_max_created_date(self.joe, contact_filter))

    def test_matches_wildcard(self):
        contact_filter = ContactFilter()
        contact_filter.search_query = "ne th"
        self.assertFalse(contact_filter.matches(self.john, contact_filter))
        self.assertTrue(contact_filter.matches(self.jane, contact_filter))
        self.assertTrue(contact_filter.matches(self.joe, contact_filter))

    def test_matches(self):
        contact_filter = ContactFilter()
        contact_filter.search_query = "John"

        self.assertTrue(ContactFilter.matches(self.john, contact_filter))
        self.assertFalse(ContactFilter.matches(self.jane, contact_filter))

        contact_filter.search_query = "ice"

        self.assertFalse(ContactFilter.matches(self.john, contact_filter))
        self.assertFalse(ContactFilter.matches(self.jane, contact_filter))


if __name__ == '__main__':
    unittest.main()
