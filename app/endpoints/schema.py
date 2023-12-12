from client_auth.models import Client, AnimalKind, Patient
from ninja import Schema


class ContactInformation(Schema):
    type: str = None  # ADDRESS, PHONE_NUMBER, EMAIL, SKYPE, WEB_ADDRESS, FAX, OTHER
    title: str = None
    value: str = None
    channel: str = None
    authorization: bool = None


class ClientSchema(Schema):
    enote_id: str = None
    state: str = None
    is_confirmed: bool = None
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    contact_information: list[ContactInformation] = None
    attributes: list[dict] = None


class ClientResponseSchema(Schema):
    enote_id: str
    result: bool
    error_message: str = None
