from ninja import NinjaAPI
from ninja.security import HttpBasicAuth
from django.conf import settings
from endpoints.api import client_router
from endpoints.export_api import export_router


class ClientBasicAuth(HttpBasicAuth):
    async def authenticate(self, request, username, password):
        if username == settings.API_USERNAME and password == settings.API_PASSWORD:
            return username


class ExportBasicAuth(HttpBasicAuth):
    async def authenticate(self, request, username, password):
        if username == settings.EXPORT_API_USERNAME and password == settings.EXPORT_API_PASSWORD:
            return username


api = NinjaAPI()

api.add_router("v1/integration/", client_router, auth=ClientBasicAuth())
api.add_router("v1/export/", export_router, auth=ExportBasicAuth())
