"""
This module contains the definition of the PhoneBookController entry
"""
from typing import Optional, Dict, Set

from exceptions.exceptions import TerminateActionLoopException, BasePhoneBookException
from phone_book.actions.action import Action, ContactCreateAction, ExitAction
from phone_book.phone_book import PhoneBook


class PhoneBookController:
    __DEFAULT_ACTIONS = [
        ContactCreateAction,
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
        print("\nActions:")
        for index, action in self.__actions.items():
            print(index, "-", action.name)

    def run(self):
        while True:
            self.show_actions()
            choice = input("Select an action: ")
            if choice not in self.__actions:
                print("Invalid choice. Please select a valid action.")
                continue
            action = self.__actions[choice]
            try:
                action.execute(self.phone_book)
            except TerminateActionLoopException:
                print("Bye")
                break
            except BasePhoneBookException as e:
                print("The following error occurred: %s" % e)
                continue
