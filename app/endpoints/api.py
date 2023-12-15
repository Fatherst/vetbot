from .schemas import ClientEnote, Result, Response, Kind
from client_auth.models import Client, AnimalKind
from typing import List
from ninja import Router
import re


router = Router()


async def create_or_update_client(client: ClientEnote, contact_information: list):
    try:
        defaults = {
            "first_name": client.first_name,
            "middle_name": client.middle_name,
            "last_name": client.last_name,
        }
        for contact in contact_information:
            if contact.type == "PHONE_NUMBER":
                phone_number = re.sub(r"\D", "", contact.value)
                defaults["phone_number"] = phone_number
                client_instance = await Client.objects.filter(
                    phone_number=phone_number,
                ).afirst()
                """Енот ID должен тогда быть null или принимать какое-то значение по умолчанию"""
                if client_instance and client_instance.enote_id == "":
                    client_instance.enote_id = client.enote_id
                    client_instance.first_name = client.first_name
                    client_instance.middle_name = client.middle_name
                    client_instance.last_name = client.last_name
                    await client_instance.asave()
            elif contact.type == "EMAIL":
                defaults["email"] = contact.value
        client_instance, created = await Client.objects.aupdate_or_create(
            enote_id=client.enote_id, defaults=defaults
        )
        success_message = (
            "Клиент успешно создан" if created else "Клиент успешно обновлен"
        )
        return Result(
            enote_id=client.enote_id,
            result=True,
            error_message=success_message,
        )
    except Exception as error:
        return Result(
            enote_id=client.enote_id,
            result=False,
            error_message=error,
        )


@router.post("integration/clients/", response=Response)
async def process_clients(request, clients: List[ClientEnote]):
    clients_response = Response(response=[])
    for client in clients:
        contact_information = client.contact_information
        clients_response.response.append(
            await create_or_update_client(client, contact_information)
        )
    return clients_response


@router.post("integration/kinds/", response=Response)
async def process_kinds(request, kinds: List[Kind]):
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
            kinds_response.response.append(
                Result(
                    enote_id=kind.enote_id,
                    result=True,
                    error_message=success_message,
                )
            )
        except Exception as error:
            return Result(
                enote_id=kind.enote_id,
                result=False,
                error_message=error,
            )
    return kinds_response
