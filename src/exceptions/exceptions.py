class BasePhoneBookException(RuntimeError):
    """This exception is to be used for all sub errors of the phone book"""


class TerminateActionLoopException(BasePhoneBookException):
    """This exception is used to terminate the work of the phone book action loop"""


class InvalidPhoneNumberException(BasePhoneBookException):
    """Throw when the phone number is not valid"""


class InvalidEmailException(BasePhoneBookException):
    """Throw when the email is not valid"""
