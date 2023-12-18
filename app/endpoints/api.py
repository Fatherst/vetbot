from .schemas import (
    ClientEnote,
    Result,
    Response,
    Kind,
)
from client_auth.models import Client, AnimalKind
from ninja import Router
import re


router = Router()


async def create_or_update_client(enote_client: ClientEnote):
    try:
        deleted = True if enote_client.state == "DELETED" else False
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
            enoteId=enote_client.enote_id,
            result=True,
            errorMessage="",
        )
    except Exception as error:
        return Result(enoteId=enote_client.enote_id, result=False, errorMessage=error)


@router.post("clients", response=Response)
async def process_clients(request, clients: list[ClientEnote]):
    clients_response = Response(response=[])
    for client in clients:
        clients_response.response.append(await create_or_update_client(client))
    return clients_response


async def create_or_update_kind(enote_kind: Kind):
    try:
        defaults = {
            "name": enote_kind.name,
        }
        _, created = await AnimalKind.objects.aupdate_or_create(
            enote_id=enote_kind.enote_id, defaults=defaults
        )
        return Result(enoteId=enote_kind.enote_id, result=True, errorMessage="")
    except Exception as error:
        return Result(enoteId=enote_kind.enote_id, result=False, errorMessage="")


@router.post("kinds", response=Response)
async def process_kinds(request, kinds: list[Kind]):
    kinds_response = Response(response=[])
    for kind in kinds:
        kinds_response.response.append(await create_or_update_kind(kind))
    return kinds_response
