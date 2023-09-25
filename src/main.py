from phone_book.phone_book import PhoneBook
from phone_book.phone_book_controller import PhoneBookController


def main():
    phone_book = PhoneBook.from_file("/home/artak/Documents/python/gng5300-assignment-1/a.csv")
    controller = PhoneBookController(phone_book)
    controller.run()


if __name__ == "__main__":
    main()
