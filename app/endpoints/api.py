import re
from appointment import models as appointment_models
from bonuses import models as bonus_models
from client_auth import models as client_models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from endpoints import schemas
from ninja import Router
from bot.classes import Phone
from bot.bot_init import logger


client_router = Router()


async def create_or_update_client(enote_client: schemas.Client) -> schemas.Result:
    try:
        deleted = True if enote_client.state == "DELETED" else False
        contact_information = enote_client.contact_information
        phone = None
        email = None
        client = None
        for contact in contact_information:
            if contact.type == "PHONE_NUMBER":
                formatted_phone = Phone.format(contact.value)
                if Phone.validate(formatted_phone):
                    phone = formatted_phone
                else:
                    raise ValidationError(message=contact.value)
            elif contact.type == "EMAIL":
                try:
                    validate_email(contact.value)
                    email = contact.value
                except ValidationError:
                    pass
        ###Тут проверка на существование телефона, иначе будет ошибка при проверке __contains
        if phone:
            client = await client_models.Client.objects.filter(
                phone_number=phone
            ).afirst()
        if client and not client.enote_id:
            client.enote_id = enote_client.enote_id
            await client.asave()
        elif client and client.enote_id:
            logger.warning(f"Клиент с неуникальным номером телефона{client.enote_id}")
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
        return schemas.Result(
            enote_id=enote_client.enote_id,
            result=True,
        )
    except Exception as error:
        logger.warning(enote_client)
        return schemas.Result(
            enote_id=enote_client.enote_id, result=False, error_message=str(error)
        )


@client_router.post("clients", response=schemas.Response, by_alias=True)
async def process_clients(request, clients: list[schemas.Client]) -> schemas.Response:
    clients_response = schemas.Response(response=[])
    for client in clients:
        clients_response.response.append(await create_or_update_client(client))
    return clients_response


async def create_or_update_kind(enote_kind: schemas.Kind) -> schemas.Result:
    try:
        if enote_kind.state == "DELETED":
            await client_models.AnimalKind.objects.filter(
                enote_id=enote_kind.enote_id
            ).adelete()
            return schemas.Result(enote_id=enote_kind.enote_id, result=True)
        defaults = {
            "name": enote_kind.name,
        }
        _, created = await client_models.AnimalKind.objects.aupdate_or_create(
            enote_id=enote_kind.enote_id, defaults=defaults
        )
        return schemas.Result(enote_id=enote_kind.enote_id, result=True)
    except Exception as error:
        return schemas.Result(
            enote_id=enote_kind.enote_id, result=False, error_message=str(error)
        )


@client_router.post("kinds", response=schemas.Response, by_alias=True)
async def process_kinds(request, kinds: list[schemas.Kind]) -> schemas.Response:
    kinds_response = schemas.Response(response=[])
    for kind in kinds:
        kinds_response.response.append(await create_or_update_kind(kind))
    return kinds_response


async def create_or_update_card_categories(
    category: schemas.DiscountCardCategory,
) -> schemas.Result:
    try:
        if category.state == "DELETED":
            await bonus_models.DiscountCardCategory.objects.filter(
                enote_id=category.enote_id
            ).adelete()
            return schemas.Result(enote_id=category.enote_id, result=True)
        defaults = {
            "name": category.name,
        }
        _, created = await bonus_models.DiscountCardCategory.objects.aupdate_or_create(
            enote_id=category.enote_id, defaults=defaults
        )
        return schemas.Result(
            enote_id=category.enote_id,
            result=True,
        )
    except Exception as error:
        return schemas.Result(
            enote_id=category.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post(
    "discount_cards/categories", response=schemas.Response, by_alias=True
)
async def process_card_categories(
    request, categories: list[schemas.DiscountCardCategory]
) -> schemas.Response:
    cards_categories_response = schemas.Response(response=[])
    for category in categories:
        cards_categories_response.response.append(
            await create_or_update_card_categories(category)
        )
    return cards_categories_response


async def create_or_update_card(card: schemas.DiscountCard) -> schemas.Result:
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
        return schemas.Result(
            enote_id=card.enote_id,
            result=True,
        )
    except Exception as error:
        return schemas.Result(
            enote_id=card.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("discount_cards", response=schemas.Response, by_alias=True)
async def process_cards(request, cards: list[schemas.DiscountCard]) -> schemas.Response:
    cards_response = schemas.Response(response=[])
    for card in cards:
        cards_response.response.append(await create_or_update_card(card))
    return cards_response


async def create_or_update_doctor(doctor_enote: schemas.Doctor) -> schemas.Result:
    try:
        deleted = doctor_enote.state == "DELETED"
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
        return schemas.Result(
            enote_id=doctor_enote.enote_id,
            result=True,
        )
    except Exception as error:
        return schemas.Result(
            enote_id=doctor_enote.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("doctors", response=schemas.Response, by_alias=True)
async def process_doctors(request, doctors: list[schemas.Doctor]) -> schemas.Response:
    doctors_response = schemas.Response(response=[])
    for doctor in doctors:
        doctors_response.response.append(await create_or_update_doctor(doctor))
    return doctors_response


async def create_or_update_appointment(
    appointment: schemas.Appointment,
) -> schemas.Result:
    try:
        deleted = appointment.state == "DELETED"
        if not appointment.client_enote_id:
            return schemas.Result(
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
        return schemas.Result(
            enote_id=appointment.enote_id,
            result=True,
        )
    except Exception as error:
        return schemas.Result(
            enote_id=appointment.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("appointments", response=schemas.Response, by_alias=True)
async def process_appointments(
    request, appointments: list[schemas.Appointment]
) -> schemas.Response:
    appointments_response = schemas.Response(response=[])
    for appointment in appointments:
        appointments_response.response.append(
            await create_or_update_appointment(appointment)
        )
    return appointments_response


async def create_or_update_patient(patient: schemas.Patient) -> schemas.Result:
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
        return schemas.Result(
            enote_id=patient.enote_id,
            result=True,
        )
    except Exception as error:
        return schemas.Result(
            enote_id=patient.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("patients", response=schemas.Response, by_alias=True)
async def process_patients(
    request, patients: list[schemas.Patient]
) -> schemas.Response:
    patients_response = schemas.Response(response=[])
    for patient in patients:
        patients_response.response.append(await create_or_update_patient(patient))
    return patients_response


async def create_or_update_weighing(weighing: schemas.Weighing) -> schemas.Result:
    try:
        if weighing.state == "DELETED":
            await client_models.Weighing.objects.filter(
                enote_id=weighing.enote_id
            ).adelete()
            return schemas.Result(enote_id=weighing.enote_id, result=True)
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
        return schemas.Result(
            enote_id=weighing.enote_id,
            result=True,
        )
    except Exception as error:
        return schemas.Result(
            enote_id=weighing.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("patients/weight", response=schemas.Response, by_alias=True)
async def process_weighings(
    request, weighings: list[schemas.Weighing]
) -> schemas.Response:
    weighings_response = schemas.Response(response=[])
    for weighing in weighings:
        weighings_response.response.append(await create_or_update_weighing(weighing))
    return weighings_response


async def create_or_update_invoice(invoice: schemas.Invoice) -> schemas.Result:
    try:
        if invoice.state == "DELETED":
            await appointment_models.Invoice.objects.filter(
                enote_id=invoice.enote_id
            ).adelete()
            return schemas.Result(enote_id=invoice.enote_id, result=True)
        if not (invoice.client_enote_id and invoice.date and invoice.sum_total):
            return schemas.Result(enote_id=invoice.enote_id, result=True)
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
        return schemas.Result(
            enote_id=invoice.enote_id,
            result=True,
        )
    except Exception as error:
        return schemas.Result(
            enote_id=invoice.enote_id,
            result=False,
            error_message=str(error),
        )


@client_router.post("invoices", response=schemas.Response, by_alias=True)
async def process_invoices(
    request, invoices: list[schemas.Invoice]
) -> schemas.Response:
    invoices_response = schemas.Response(response=[])
    for invoice in invoices:
        invoices_response.response.append(await create_or_update_invoice(invoice))
    return invoices_response
