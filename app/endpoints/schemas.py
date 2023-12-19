from ninja import Schema, Field
from typing import Optional


class ContactInformation(Schema):
    type: str = None
    title: str = None
    value: str = None
    channel: str = None
    authorization: bool = None


class Kind(Schema):
    enote_id: str = Field(None, alias="enoteId")
    state: str = Field(None, alias="objectState")
    name: str = Field(None)
    kind_id: str = Field(alias="KindId")


class ClientEnote(Schema):
    enote_id: str = Field(None, alias="enoteId")
    state: str = Field(None, alias="objectState")
    is_confirmed: bool = Field(None, alias="isConfirmed")
    first_name: str = Field("", alias="firstName")
    middle_name: str = Field("", alias="middleName")
    last_name: str = Field("", alias="lastName")
    contact_information: list[ContactInformation] = None
    attributes: Optional[list[dict]] = None



class DiscountCardSchema(Schema):
    enote_id: str = Field(None, alias="enoteId")
    state: str = Field(None, alias="objectState")
    name: str = None
    client_enote_id: str = Field(None, alias="clientEnoteId")
    card_number: str = Field(None, alias="codeCard")
    category_enote_id: str = Field(None, alias="categoryOfDiscountEnoteId")
    validity_date: str = Field(None, alias="validityDate")
    description: str = Field(None, alias="cardDescription")



class DiscountCardCategorySchema(Schema):
    enote_id: str
    state: str
    name: str = None



class Result(Schema):
    enote_id: str = Field("", alias="enoteId")
    result: bool
    error_message: str = Field("", alias="errorMessage")

    class Config(Schema.Config):
        populate_by_name = True


class Response(Schema):
    response: list[Result]
