"""
This module contains the definition of the PhoneBookController entry
"""
from typing import Optional, Dict, Set

from actions.action import ContactCreateAction, ExitAction, Action, ShowContacts, DeleteContact, UpdateFilter, \
    DeleteCurrentResults, ShowCurrentContacts, ResetFilter, EditContact, GroupByLastNameFirstLetter, \
    GroupCurrentContactsByLastNameFirstLetter, ImportFromFile
from audit import get_logger_by_name
from exceptions.exceptions import TerminateActionLoopException, BasePhoneBookException
from phone_book.phone_book import PhoneBook


class PhoneBookController:
    logger = get_logger_by_name("PhoneBookController")
    __DEFAULT_ACTIONS = [
        ShowContacts,
        ContactCreateAction,
        EditContact,
        DeleteContact,
        GroupByLastNameFirstLetter,
        GroupCurrentContactsByLastNameFirstLetter,
        DeleteCurrentResults,
        ShowCurrentContacts,
        UpdateFilter,
        ResetFilter,
        ImportFromFile,
        ExitAction
    ]
    _phone_book: PhoneBook
    __actions: Dict[str, Action]

    def __init__(self, phone_book: Optional[PhoneBook] = None, actions: Set[Action] = None):
        if phone_book is None:
            phone_book = PhoneBook()
        if actions is None:
            actions = {str(index): action() for index, action in enumerate(self.__DEFAULT_ACTIONS, 1)}
            self.__actions = actions

        self._phone_book = phone_book

    @property
    def phone_book(self):
        return self._phone_book

    def show_actions(self):
        print("Actions:")
        for index, action in self.__actions.items():
            print(index, "-", action.name)

    def run(self):
        while True:
            print("#" * 80)
            self.show_actions()
            print("#" * 80)
            choice = input("Select an action: ")
            if choice not in self.__actions:
                self.logger.error("Invalid choice '%s'. Please select a valid action.", choice)
                continue
            print("*" * 60)
            action = self.__actions[choice]
            print(f"Performing action {action.name}")
            try:
                action.execute(self.phone_book)
            except TerminateActionLoopException:
                self.logger.info("Exiting")
                break
            except BasePhoneBookException as ex:
                self.logger.error("The following error occurred: %s", str(ex))
                continue
            except RuntimeError as ex:
                self.logger.error("Something went wrong: %s", str(ex))
                continue
            print("*" * 60)
