import argparse

from phone_book.phone_book import PhoneBook
from phone_book.phone_book_controller import PhoneBookController


def main():
    parser = argparse.ArgumentParser(description="Phonebook Application")
    parser.add_argument("--file-path", type=str, help="Path to a CSV file to initialize the phonebook")

    args = parser.parse_args()

    if args.file_path:
        file_path = args.file_path
        phone_book = PhoneBook.from_file(file_path)
        print(f"Phonebook initialized from '{file_path}'")
    else:
        phone_book = PhoneBook()
        print("Empty phonebook initialized")
    controller = PhoneBookController(phone_book)
    controller.run()


if __name__ == "__main__":
    main()
