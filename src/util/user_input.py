import datetime

from exceptions.exceptions import InvalidActionException, InvalidInputException


def get_boolean_from_user(message: str = "Do you want to change this value?(Type 'Yes' or 'Y' to confirm): ") -> bool:
    user_input = input(message)
    inp = user_input.lower()
    valid_yes = ['yes', 'y']
    valid_no = ['no', 'n']
    if inp in valid_yes:
        user_boolean = True
    elif inp in valid_no:
        user_boolean = False
    else:
        raise InvalidActionException("Invalid action")
    return user_boolean


def get_datetime_from_user(
        message: str,
        datetime_format: str = "%Y-%m-%d %H:%M:%S",
        format_helper: str = "YYYY-MM-DD HH:MM:SS"
) -> datetime.datetime:
    try:
        datetime_str = input(f"{message}(use {format_helper}): ")
        return datetime.datetime.strptime(datetime_str, datetime_format)
    except ValueError as error:
        raise InvalidInputException(f"Invalid datetime format. Please use {format_helper}") from error
