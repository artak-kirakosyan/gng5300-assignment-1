class BasePhoneBookException(RuntimeError):
    """This exception is to be used for all sub errors of the phone book"""


class TerminateActionLoopException(BasePhoneBookException):
    """This exception is used to terminate the work of the phone book action loop"""


class InvalidPhoneNumberException(BasePhoneBookException):
    """Throw when the phone number is not valid"""


class InvalidEmailException(BasePhoneBookException):
    """Throw when the email is not valid"""


class InvalidNameException(BasePhoneBookException):
    """Throw when the name is not valid"""


class ContactAlreadyExistsException(BasePhoneBookException):
    """Throw when the contact with a given id already exists"""


class NoContactsMatchedException(BasePhoneBookException):
    """Throw when no contacts were matched but a match was expected"""


class ContactIsNotRegisteredException(BasePhoneBookException):
    """Throw when the contact is not registered in phone book"""


class InvalidActionException(BasePhoneBookException):
    """Throw when an invalid action is selected by the user"""
