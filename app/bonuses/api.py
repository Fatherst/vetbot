from .schemas import (
    DiscountCardSchema,
    DiscountCardCategorySchema,
)
from endpoints.schemas import Result, Response
from client_auth.models import Client, AnimalKind
from .models import DiscountCardCategory, DiscountCard
from ninja import Router

bonuses_router = Router()



async def create_or_update_card_categories(
    category: DiscountCardCategorySchema,
) -> Result:
    try:
        if category.state == "DELETED":
            await DiscountCardCategory.objects.filter(enote_id=category.enote_id).adelete()
            return Result(enote_id=category.enote_id, result=True)
        defaults = {
            "name": category.name,
        }
        _, created = await DiscountCardCategory.objects.aupdate_or_create(
            enote_id=category.enote_id, defaults=defaults
        )
        return Result(
            enote_id=category.enote_id,
            result=True,
        )
    except Exception as error:
        return Result(
            enote_id=category.enote_id,
            result=False,
            error_message=str(error),
        )


@bonuses_router.post("discount_cards/categories", response=Response, by_alias=True)
async def process_card_categories(
    request, categories: list[DiscountCardCategorySchema]
):
    cards_categories_response = Response(response=[])
    for category in categories:
        cards_categories_response.response.append(
            await create_or_update_card_categories(category)
        )
    return cards_categories_response


async def create_or_update_card(card: DiscountCardSchema) -> Result:
    try:
        deleted = True if card.state == "DELETED" else False
        client = await Client.objects.aget(enote_id=card.client_enote_id)
        category = await DiscountCardCategory.objects.aget(
            enote_id=card.category_enote_id
        )
        defaults = {
            "card_number": card.card_number,
            "client": client,
            "category": category,
            "deleted": deleted,
        }
        _, created = await DiscountCard.objects.aupdate_or_create(
            enote_id=card.enote_id, defaults=defaults
        )
        return Result(
            enote_id=card.enote_id,
            result=True,
        )
    except Exception as error:
        return Result(
            enote_id=card.enote_id,
            result=False,
            error_message=str(error),
        )


@bonuses_router.post("discount_cards", response=Response, by_alias=True)
async def process_cards(request, cards: list[DiscountCardSchema]):
    cards_response = Response(response=[])
    for card in cards:
        cards_response.response.append(await create_or_update_card(card))
    return cards_response