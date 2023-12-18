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


async def result(schema_instance, success_message: str, res_bool: bool):
    return Result(
        enote_id=schema_instance.enote_id,
        result=res_bool,
        error_message=success_message,
    )


async def create_or_update_client(enote_client: ClientEnote):
    try:
        if enote_client.state == "DELETED":
            client = await Client.objects.aget(enote_id=enote_client.enote_id)
            client.deleted = True
            await client.asave()
            return await result(enote_client, "Клиент успешно удалён",True)
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
            'email': email,
            'phone_number': phone
        }
        _, created = await Client.objects.aupdate_or_create(
            enote_id=enote_client.enote_id, defaults=defaults
        )
        success_message = (
            "Клиент успешно создан" if created else "Клиент успешно обновлен"
        )
        return await result(enote_client, success_message, True)
    except Exception as error:
        return await result(enote_client, str(error), False)


@router.post("clients", response=Response)
async def process_clients(request, clients: list[ClientEnote]):
    clients_response = Response(response=[])
    for client in clients:
        clients_response.response.append(await create_or_update_client(client))
    return clients_response


@router.post("kinds", response=Response)
async def process_kinds(request, kinds: list[Kind]):
    kinds_response = Response(response=[])
    for kind in kinds:
        try:
            defaults = {
                "name": kind.name,
            }
            kind_instance, created = await AnimalKind.objects.aupdate_or_create(
                enote_id=kind.enote_id, defaults=defaults
            )
            success_message = (
                "Вид успешно создан" if created else "Вид успешно обновлен"
            )
            kinds_response.response.append(await result(kind, success_message, True))
        except Exception as error:
            return await result(kind, str(error), False)
    return kinds_response
