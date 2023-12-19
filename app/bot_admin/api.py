from ninja import NinjaAPI
from ninja.security import HttpBasicAuth
from django.conf import settings
from endpoints.api import client_router
from bonuses.api import bonuses_router


class BasicAuth(HttpBasicAuth):
    async def authenticate(self, request, username, password):
        if username == settings.API_USERNAME and password == settings.API_PASSWORD:
            return username


api = NinjaAPI(auth=BasicAuth())

api.add_router("v1/integration/", client_router)
api.add_router("v1/integration/", bonuses_router)
