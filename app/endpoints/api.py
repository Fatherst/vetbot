from django.shortcuts import render
from ninja import NinjaAPI
from .schema import ClientSchema, PatientSchema,KindSchema
from .models import Kind, Patient,Breed
from client_auth.models import Client

api = NinjaAPI()


@api.get("v1/integration/clients/{client_enote_id}",response={200: ClientSchema})
def client(request, client_enote_id: str):
    try:
        client = Client.objects.get(client_enote_id=client_enote_id)
        return 200, client
    except Client.DoesNotExist as e:
        return 404,{"message": "Client does not exist"}

@api.get("v1/integration/test")
def client(request):
    return {'test':'succes'}

@api.post("v1/integration/clients",response={201: ClientSchema})
def create_client(request, client: ClientSchema):
    client = Client.objects.create(**client.dict())
    return client

@api.post("v1/integration/patients",response={201: PatientSchema})
def create_patient(request, patient: PatientSchema):
    patient = Patient.objects.create(**patient.dict())
    return patient

@api.post("v1/integration/kinds",response={201: KindSchema})
def create_patient(request, patient: KindSchema):
    patient = Kind.objects.create(**patient.dict())
    return patient

# @api.post("v1/integration/appointments", response={201: AppointmentSchema})
# def create_appointment(request, appointment: AppointmentSchema):
#     appointment = Appointment.objects.create(**appointment.dict())
#     return appointment