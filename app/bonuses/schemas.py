from ninja import Schema, Field


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