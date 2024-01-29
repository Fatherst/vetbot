import csv
import io
from datetime import datetime
from django.utils import timezone
import pytz

from asgiref.sync import sync_to_async
from django.http import HttpResponse, StreamingHttpResponse
from ninja import Router
import re
import logging
from .schemas import (
    Client,
    Result,
    Response,
    Kind,
    DiscountCardCategory,
    DiscountCard,
    Doctor,
    Appointment,
    Patient,
    Weighing,
    Invoice,
)
from bonuses import models as bonus_models
from client_auth import models as client_models
from appointment import models as appointment_models


logger = logging.getLogger(__name__)


client_router = Router()


async def create_or_update_client(enote_client: Client) -> Result:
    try:
        deleted = True if enote_client.state == "DELETED" else False
        contact_information = enote_client.contact_information
        phone = None
        email = None
        client = None
        for contact in contact_information:
            if contact.type == "PHONE_NUMBER":
                phone = re.sub(r"\D", "", contact.value)
            elif contact.type == "EMAIL":
                email = contact.value
        ###Тут проверка на существование телефона, иначе будет ошибка при проверке __contains
        if phone:
            client = await client_models.Client.objects.filter(
                phone_number__contains=phone[1:]
            ).afirst()
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
        _, created = await client_models.Client.objects.aupdate_or_create(
            enote_id=enote_client.enote_id, defaults=defaults
        )
        return Result(
            enote_id=enote_client.enote_id,
            result=True,
        )
    except Exception as error:
        logger.error(enote_client)
        return Result(
            enote_id=enote_client.enote_id, result=False, error_message=str(error)
        )


@client_router.post("clients", response=Response, by_alias=True)
async def process_clients(request, clients: list[Client]) -> Response:
    clients_response = Response(response=[])
    for client in clients:
        clients_response.response.append(await create_or_update_client(client))
    return clients_response


async def create_or_update_kind(enote_kind: Kind) -> Result:
    try:
        if enote_kind.state == "DELETED":
            await client_models.AnimalKind.objects.filter(
                enote_id=enote_kind.enote_id
            ).adelete()
            return Result(enote_id=enote_kind.enote_id, result=True)
        defaults = {
            "name": enote_kind.name,
        }
        _, created = await client_models.AnimalKind.objects.aupdate_or_create(
            enote_id=enote_kind.enote_id, defaults=defaults
        )
        return Result(enote_id=enote_kind.enote_id, result=True)
    except Exception as error:
        return Result(
            enote_id=enote_kind.enote_id, result=False, error_message=str(error)
        )


@client_router.post("kinds", response=Response, by_alias=True)
async def process_kinds(request, kinds: list[Kind]) -> Response:
    kinds_response = Response(response=[])
    for kind in kinds:
        kinds_response.response.append(await create_or_update_kind(kind))
    return kinds_response


async def create_or_update_card_categories(
    category: DiscountCardCategory,
) -> Result:
    try:
        if category.state == "DELETED":
            await bonus_models.DiscountCardCategory.objects.filter(
                enote_id=category.enote_id
            ).adelete()
            return Result(enote_id=category.enote_id, result=True)
        defaults = {
            "name": category.name,
        }
        _, created = await bonus_models.DiscountCardCategory.objects.aupdate_or_create(
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


@client_router.post("discount_cards/categories", response=Response, by_alias=True)
async def process_card_categories(
    request, categories: list[DiscountCardCategory]
) -> Response:
    cards_categories_response = Response(response=[])
    for category in categories:
        cards_categories_response.response.append(
            await create_or_update_card_categories(category)
        )
    return cards_categories_response


async def create_or_update_card(card: DiscountCard) -> Result:
    try:
        deleted = True if card.state == "DELETED" else False
        client = None
        category = None
        client = await client_models.Client.objects.filter(
            enote_id=card.client_enote_id
        ).afirst()
        category = await bonus_models.DiscountCardCategory.objects.filter(
            enote_id=card.category_enote_id
        ).afirst()
        defaults = {
            "card_number": card.card_number,
            "client": client,
            "category": category,
            "deleted": deleted,
        }
        _, created = await bonus_models.DiscountCard.objects.aupdate_or_create(
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


@client_router.post("discount_cards", response=Response, by_alias=True)
async def process_cards(request, cards: list[DiscountCard]) -> Response:
    cards_response = Response(response=[])
    for card in cards:
        cards_response.response.append(await create_or_update_card(card))
    return cards_response


async def create_or_update_doctor(doctor_enote: Doctor) -> Result:
    try:
        deleted = doctor_enote.state == "DELETED"
        specializations = []
        for specialization in doctor_enote.specialization:
            (
                spec,
                created,
            ) = await appointment_models.Specialization.objects.aupdate_or_create(
                enote_id=specialization.enote_id,
                defaults={"name": specialization.title},
            )
            specializations.append(spec)
        defaults = {
            "first_name": doctor_enote.first_name,
            "middle_name": doctor_enote.middle_name,
            "last_name": doctor_enote.last_name,
            "fired_date": doctor_enote.fired_date,
            "deleted": deleted,
        }
        doctor, created = await appointment_models.Doctor.objects.aupdate_or_create(
            enote_id=doctor_enote.enote_id, defaults=defaults
        )
        if specializations:
            await doctor.specializations.aset(specializations)
        return Result(
            enote_id=doctor_enote.enote_id,
            result=True,
        )
    except Exception as error:
        return Result(
            enote_id=doctor_enote.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("doctors", response=Response, by_alias=True)
async def process_doctors(request, doctors: list[Doctor]) -> Response:
    doctors_response = Response(response=[])
    for doctor in doctors:
        doctors_response.response.append(await create_or_update_doctor(doctor))
    return doctors_response


async def create_or_update_appointment(appointment: Appointment) -> Result:
    try:
        deleted = appointment.state == "DELETED"
        if not appointment.client_enote_id:
            return Result(
                enote_id=appointment.enote_id,
                result=True,
            )
        client = await client_models.Client.objects.aget(
            enote_id=appointment.client_enote_id
        )
        patient = await client_models.Patient.objects.filter(
            enote_id=appointment.patient_enote_id
        ).afirst()
        doctor = await appointment_models.Doctor.objects.filter(
            enote_id=appointment.doctor_enote_id
        ).afirst()
        defaults = {
            "status": appointment.status,
            "patient": patient,
            "doctor": doctor,
            "client": client,
            "date_time": appointment.start_time,
            "deleted": deleted,
        }
        _, created = await appointment_models.Appointment.objects.aupdate_or_create(
            enote_id=appointment.enote_id, defaults=defaults
        )
        return Result(
            enote_id=appointment.enote_id,
            result=True,
        )
    except Exception as error:
        return Result(
            enote_id=appointment.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("appointments", response=Response, by_alias=True)
async def process_appointments(request, appointments: list[Appointment]) -> Response:
    appointments_response = Response(response=[])
    for appointment in appointments:
        appointments_response.response.append(
            await create_or_update_appointment(appointment)
        )
    return appointments_response


async def create_or_update_patient(patient: Patient) -> Result:
    try:
        deleted = patient.state == "DELETED"
        client = await client_models.Client.objects.aget(
            enote_id=patient.client_enote_id
        )
        kind = await client_models.AnimalKind.objects.aget(
            enote_id=patient.kind_enote_id
        )
        defaults = {
            "kind": kind,
            "client": client,
            "birth_date": patient.birth_date,
            "name": patient.name,
            "time_of_death": patient.time_of_death,
            "deleted": deleted,
        }
        _, created = await client_models.Patient.objects.aupdate_or_create(
            enote_id=patient.enote_id, defaults=defaults
        )
        return Result(
            enote_id=patient.enote_id,
            result=True,
        )
    except Exception as error:
        return Result(
            enote_id=patient.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("patients", response=Response, by_alias=True)
async def process_patients(request, patients: list[Patient]) -> Response:
    patients_response = Response(response=[])
    for patient in patients:
        patients_response.response.append(await create_or_update_patient(patient))
    return patients_response


async def create_or_update_weighing(weighing: Weighing) -> Result:
    try:
        if weighing.state == "DELETED":
            await client_models.Weighing.objects.filter(
                enote_id=weighing.enote_id
            ).adelete()
            return Result(enote_id=weighing.enote_id, result=True)
        patient = await client_models.Patient.objects.aget(
            enote_id=weighing.patient_enote_id
        )
        defaults = {
            "patient": patient,
            "weight": weighing.weight,
            "date": weighing.date,
        }
        _, created = await client_models.Weighing.objects.aupdate_or_create(
            enote_id=weighing.enote_id, defaults=defaults
        )
        return Result(
            enote_id=weighing.enote_id,
            result=True,
        )
    except Exception as error:
        return Result(
            enote_id=weighing.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("patients/weight", response=Response, by_alias=True)
async def process_weighings(request, weighings: list[Weighing]) -> Response:
    weighings_response = Response(response=[])
    for weighing in weighings:
        weighings_response.response.append(await create_or_update_weighing(weighing))
    return weighings_response


async def create_or_update_invoice(invoice: Invoice) -> Result:
    try:
        if invoice.state == "DELETED":
            await appointment_models.Invoice.objects.filter(
                enote_id=invoice.enote_id
            ).adelete()
            return Result(enote_id=invoice.enote_id, result=True)
        if not (invoice.client_enote_id and invoice.date and invoice.sum_total):
            return Result(enote_id=invoice.enote_id, result=True)
        client = await client_models.Client.objects.aget(
            enote_id=invoice.client_enote_id
        )
        defaults = {
            "client": client,
            "date": invoice.date,
            "sum": invoice.sum_total,
        }
        _, created = await appointment_models.Invoice.objects.aupdate_or_create(
            enote_id=invoice.enote_id, defaults=defaults
        )
        return Result(
            enote_id=invoice.enote_id,
            result=True,
        )
    except Exception as error:
        return Result(
            enote_id=invoice.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("invoices", response=Response, by_alias=True)
async def process_invoices(request, invoices: list[Invoice]) -> Response:
    invoices_response = Response(response=[])
    for invoice in invoices:
        invoices_response.response.append(await create_or_update_invoice(invoice))
    return invoices_response


@client_router.get("csv/invoices")
async def export_csv(request) -> StreamingHttpResponse:
    csv_buffer = io.StringIO()
    fieldnames = [
        "InvoicePaymentDate",
        "ClientEnoteId",
        "Email",
        "Phone_number",
        "InvoicePaymentTotal",
        "NewClient",
    ]
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    start_date = datetime(2024, 1, 8, tzinfo=pytz.UTC)
    # Получаем данные из базы данных
    invoices = await sync_to_async(list)(
        appointment_models.Invoice.objects.filter(
            date__range=[start_date, timezone.now()]
        )
        .select_related("client")
        .all()
    )
    for invoice in invoices:
        # Проверяем, является ли инвойс первым у клиента
        is_first_invoice = not await sync_to_async(
            (appointment_models.Invoice.objects.filter)(
                client=invoice.client, date__lt=invoice.date
            ).exists
        )()
        phone_number = invoice.client.phone_number
        if phone_number[0] == "8":
            phone_number = f"7{phone_number[1:]}"
        email = invoice.client.email
        csv_data = {
            "InvoicePaymentDate": invoice.date.strftime("%Y-%m-%d %H:%M:%S"),
            "ClientEnoteId": invoice.client.enote_id,
            "Email": email,
            "Phone_number": phone_number,
            "InvoicePaymentTotal": str(invoice.sum),
            "NewClient": "True" if is_first_invoice else "False",
        }
        writer.writerow(csv_data)
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()
    response = HttpResponse(csv_content, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="exported_data.csv"'
    return response
