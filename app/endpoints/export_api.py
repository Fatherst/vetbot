import csv
import re
from datetime import datetime, timedelta
from django.utils import timezone
from asgiref.sync import sync_to_async
from django.http import HttpResponse
from ninja import Router
import logging
from appointment import models as appointment_models


logger = logging.getLogger(__name__)


export_router = Router()


@export_router.get("invoices")
async def export_csv(request, period: int = 5) -> HttpResponse:
    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="invoices_'
            f'{timezone.now().strftime("%Y_%m_%d")}.csv"'
        },
    )
    writer = csv.writer(response, delimiter=";")

    fieldnames = [
        "create_date_time",
        "id",
        "emails",
        "phones",
        "revenue",
        "order_status",
    ]
    writer.writerow(fieldnames)
    start_date = datetime.now() - timedelta(days=period)
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
        if phone_number and phone_number[0] == "8":
            phone_number = f"7{phone_number[1:]}"
        email = invoice.client.email
        if email and not re.match(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email
        ):
            email = None
        csv_data = [
            invoice.date.strftime("%d.%m.%Y %H:%M"),
            invoice.client.enote_id,
            email,
            phone_number,
            invoice.sum,
            "IN_PROGRESS" if is_first_invoice else "PAID",
        ]
        writer.writerow(csv_data)
    return response
