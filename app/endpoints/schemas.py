from ninja import Schema, Field
from typing import Optional


def to_camel(string: str) -> str:
    words = string.split("_")
    camel_case = "".join(words[0]) + "".join(word.capitalize() for word in words[1:])
    return camel_case


class ContactInformation(Schema):
    type: str = None
    title: str = None
    value: str = None
    channel: str = None
    authorization: bool = None


class Kind(Schema):
    enote_id: str = Field(None, alias="enoteId")
    object_state: str = Field(None, alias="objectState")
    name: str = Field(None)
    kind_id: str = Field(alias="KindId")


class ClientEnote(Schema):
    enote_id: str = Field(None, alias="enoteId")
    object_state: str = Field(None, alias="objectState")
    is_confirmed: bool = Field(None, alias="isConfirmed")
    first_name: str = Field("", alias="firstName")
    middle_name: str = Field("", alias="middleName")
    last_name: str = Field("", alias="lastName")
    contact_information: list[ContactInformation] = None
    attributes: Optional[list[dict]] = None

    class Config(Schema.Config):
        alias_generator = to_camel
        populate_by_name = True


class DiscountCardSchema(Schema):
    enote_id: str = Field(None, alias="enoteId")
    object_state: str = Field(None, alias="objectState")
    name: str = None
    client_enote_id: str = Field(None, alias="clientEnoteId")
    code_card: str = Field(None, alias="codeCard")
    category_of_discount_enote_id: str = Field(None, alias="categoryOfDiscountEnoteId")
    validity_date: str = Field(None, alias="validityDate")
    card_description: str = Field(None, alias="cardDescription")

    class Config(Schema.Config):
        alias_generator = to_camel
        populate_by_name = True


class DiscountCardCategorySchema(Schema):
    enote_id: str
    object_state: str
    name: str = None

    class Config(Schema.Config):
        alias_generator = to_camel
        populate_by_name = True


class Result(Schema):
    enote_id: str
    result: bool
    error_message: str = ""

    class Config(Schema.Config):
        alias_generator = to_camel
        populate_by_name = True


class Response(Schema):
    response: list[Result]
