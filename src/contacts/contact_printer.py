from contacts.contact import Contact


class ContactPrinter:
    def __init__(self, indent_size: int = 20):
        self._indent_size = indent_size

    def get_headers(self) -> str:
        header_line = f'{"id": <{40}} ' \
                       f'{"first_name": <{self._indent_size}} ' \
                       f'{"last_name": <{self._indent_size}} ' \
                       f'{"phone_number": <{self._indent_size}} ' \
                       f'{"email": <{self._indent_size}} ' \
                       f'{"address": <{self._indent_size}}'
        return header_line

    def to_line(self, contact: Contact) -> str:
        email = contact.email if contact.email is not None else "--"
        address = contact.address if contact.address is not None else "--"

        contact_line = f'{contact.contact_id: <{40}} ' \
                       f'{contact.first_name: <{self._indent_size}} ' \
                       f'{contact.last_name: <{self._indent_size}} ' \
                       f'{contact.phone_number: <{self._indent_size}} ' \
                       f'{email: <{self._indent_size}} ' \
                       f'{address: <{self._indent_size}}'
        return contact_line
