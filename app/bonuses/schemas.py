from ninja import Schema, Field


class DiscountCard(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    name: str = None
    client_enote_id: str = Field(None, alias="clientEnoteId")
    card_number: str = Field(None, alias="codeCard")
    category_enote_id: str = Field(None, alias="categoryOfDiscountEnoteId")
    validity_date: str = Field(None, alias="validityDate")
    description: str = Field(None, alias="cardDescription")


class DiscountCardCategory(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    name: str = None


class BonusPoints(Schema):
    discount_card_enote_id: str = Field(alias="discountCardEnoteId")
    date: str = Field(alias="eventDate")
    sum: int


class BonusTransaction(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(alias="objectState")
    operation_type: str = Field(alias="discountOperationType")
    department_enote_id: str = Field(alias="departmentEnoteId")
    description: str = Field(None, alias="description")
    bonus_points: list[BonusPoints] = Field(alias="bonusPoints")
