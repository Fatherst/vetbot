from bonuses.models import BonusAccrual, Program
from bot_admin.celery import app
from client_auth.models import Patient
from django.utils import timezone
from integrations.enote.methods import add_bonus_points


@app.task
def accrual_bonuses_by_enote(accrual_id):
    accrual = BonusAccrual.objects.get(id=accrual_id)

    discount_card = accrual.client.discount_card
    if not discount_card:
        return

    enote_accrued = add_bonus_points(
        discount_card.enote_id,
        accrual.reason,
        accrual.amount,
        str(accrual.created_at),
    )
    if enote_accrued:
        accrual.accrued = True
        accrual.save()


@app.task
def process_not_accrued_bonuses():
    accruals = BonusAccrual.objects.filter(accrued=False)
    for accrual in accruals:
        accrual_bonuses_by_enote.delay(accrual.id)


@app.task
def process_patients_birthdays():
    try:
        active_program = Program.objects.get(is_active=True)
    except Program.DoesNotExist:
        return

    today = timezone.now().date()
    patients = (
        Patient.objects.filter(
            birth_date__day=today.day,
            birth_date__month=today.month,
            time_of_death=None,
        )
        .exclude(deleted=True)
        .exclude(client__in_blacklist__isnull=False)
    )

    for patient in patients:
        bonus_not_accrued_before = not BonusAccrual.objects.filter(
            client=patient.client, reason="BIRTHDAY", created_at__year=today.year
        ).exists()
        if patient.client.with_discount_card and bonus_not_accrued_before:
            BonusAccrual.objects.create(
                client=patient.client,
                reason="BIRTHDAY",
                amount=active_program.birthday_bonus_amount,
            )
