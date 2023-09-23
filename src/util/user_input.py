from exceptions.exceptions import InvalidActionException


def get_boolean_from_user(message: str) -> bool:
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
