from contacts.contact import Contact
from phone_book.phone_book import PhoneBook
from phone_book.phone_book_controller import PhoneBookController


def main():
    contacts = [
        Contact("Artak", "Kirakosyan", "(443) 234-1313"),
        Contact("Artak", "Kirakosyan", "(443) 234-1313", "akira@uottawea.ca")
    ]
    phone_book = PhoneBook(contacts)
    controller = PhoneBookController(phone_book)
    controller.run()


if __name__ == "__main__":
    main()
