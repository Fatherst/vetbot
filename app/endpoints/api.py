from ninja import NinjaAPI
from .schema import ClientSchema, ClientResponseSchema
from client_auth.models import Client
from ninja.security import HttpBasicAuth
from django.conf import settings



class BasicAuth(HttpBasicAuth):
    async def authenticate(self, request, username, password):
        if username == settings.API_USERNAME and password == settings.API_PASSWORD:
            return username


api = NinjaAPI(auth=BasicAuth())


async def create_client_with_contact_info(client, **kwargs):
    client_data = {
        "first_name": client.first_name,
        "middle_name": client.middle_name,
        "last_name": client.last_name,
        "enote_id": client.enote_id,
        **kwargs,
    }
    await Client.objects.acreate(**client_data)


@api.post("v1/integration/clients/", response=ClientResponseSchema)
async def post_client(request, client: ClientSchema):
    try:
        client_dict = client.dict()
        if await Client.objects.filter(enote_id=client.enote_id).afirst():
            return {
                "enote_id": client.enote_id,
                "result": False,
                "error_message": "Клиент с таким enote_id уже существует",
            }
        contact_information = client_dict["contact_information"][0]
        if contact_information.get("type") == "PHONE_NUMBER":
            phone_number = contact_information.get("value")
            client_from_db = await Client.objects.filter(
                phone_number=phone_number
            ).afirst()
            if client_from_db:
                client_from_db.enote_id = client.enote_id
                await client_from_db.asave()
                return {
                    "enote_id": client.enote_id,
                    "result": False,
                    "error_message": "Клиент с таким номером телефона уже существует",
                }
            await create_client_with_contact_info(client, phone_number=phone_number)
            return {
                "enote_id": client.enote_id,
                "result": True,
                "error_message": "Клиент с номером телефона успешно создан",
            }
        elif contact_information.get("type") == "EMAIL":
            await create_client_with_contact_info(
                client, email=contact_information.get("value")
            )
            return {
                "enote_id": client.enote_id,
                "result": True,
                "error_message": "Клиент с адресом электронной почты успешно создан",
            }
        return {
            "enote_id": client.enote_id,
            "result": False,
            "error_message": "Нет контактных данных",
        }
    except Exception as e:
        return {"error": "Произошла ошибка", "details": str(e)}
