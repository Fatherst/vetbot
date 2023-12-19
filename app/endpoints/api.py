from .schemas import (
    ClientEnote,
    Result,
    Response,
    Kind,
    DiscountCardSchema,
    DiscountCardCategorySchema,
)
from client_auth.models import Client, AnimalKind, DiscountCardCategory, DiscountCard
from ninja import Router
import re


router = Router()


async def create_or_update_client(enote_client: ClientEnote):
    try:
        deleted = True if enote_client.object_state == "DELETED" else False
        contact_information = enote_client.contact_information
        phone = None
        email = None
        for contact in contact_information:
            if contact.type == "PHONE_NUMBER":
                phone = re.sub(r"\D", "", contact.value)
            elif contact.type == "EMAIL":
                email = contact.value
        client = await Client.objects.filter(phone_number=phone).afirst()
        if client and not client.enote_id:
            client.enote_id = enote_client.enote_id
            await client.asave()
        defaults = {
            "first_name": enote_client.first_name,
            "middle_name": enote_client.middle_name,
            "last_name": enote_client.last_name,
            "email": email,
            "phone_number": phone,
            "deleted": deleted,
        }
        _, created = await Client.objects.aupdate_or_create(
            enote_id=enote_client.enote_id, defaults=defaults
        )
        return Result(
            enote_id=enote_client.enote_id,
            result=True,
        )
    except Exception as error:
        return Result(enote_id=enote_client.enote_id, result=False, error_message=error)


@router.post("clients", response=Response, by_alias=True)
async def process_clients(request, clients: list[ClientEnote]):
    clients_response = Response(response=[])
    for client in clients:
        clients_response.response.append(await create_or_update_client(client))
    return clients_response


async def create_or_update_kind(enote_kind: Kind):
    try:
        if enote_kind.object_state == "DELETED":
            await AnimalKind.objects.adelete(enote_id=enote_kind.enote_id)
            return Result(enote_id=enote_kind.enote_id, result=True)
        defaults = {
            "name": enote_kind.name,
        }
        _, created = await AnimalKind.objects.aupdate_or_create(
            enote_id=enote_kind.enote_id, defaults=defaults
        )
        return Result(enote_id=enote_kind.enote_id, result=True)
    except Exception as error:
        return Result(enote_id=enote_kind.enote_id, result=False, error_message=error)


@router.post("kinds", response=Response)
async def process_kinds(request, kinds: list[Kind]):
    kinds_response = Response(response=[])
    for kind in kinds:
        kinds_response.response.append(await create_or_update_kind(kind))
    return kinds_response


async def create_or_update_card_categories(category: DiscountCardCategorySchema):
    try:
        if category.object_state == "DELETED":
            await DiscountCardCategory.objects.adelete(enote_id=category.enote_id)
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
            error_message=error,
        )


@router.post("discount_cards/categories", response=Response, by_alias=True)
async def process_card_categories(
    request, categories: list[DiscountCardCategorySchema]
):
    cards_categories_response = Response(response=[])
    for category in categories:
        cards_categories_response.response.append(
            await create_or_update_card_categories(category)
        )
    return cards_categories_response


async def create_or_update_card(card: DiscountCardSchema):
    try:
        deleted = True if card.object_state == "DELETED" else False
        client = await Client.objects.aget(enote_id=card.client_enote_id)
        category = await DiscountCardCategory.objects.aget(
            enote_id=card.category_of_discount_enote_id
        )
        defaults = {
            "card_number": card.code_card,
            "client_id": client,
            "category_id": category,
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
            error_message=error,
        )


@router.post("discount_cards", response=Response, by_alias=True)
async def process_cards(request, cards: list[DiscountCardSchema]):
    cards_response = Response(response=[])
    for card in cards:
        cards_response.response.append(await create_or_update_card(card))
    return cards_response
