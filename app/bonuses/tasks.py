from celery import shared_task
import logging
from bonuses.models import BonusAccrual
from integrations.enote.methods import add_bonus_points
from bot_admin.celery import app

logger = logging.getLogger(__name__)


@app.task
def accrual_bonuses_by_enote(accrual_id):
    accrual = BonusAccrual.objects.get(id=accrual_id)
    enote_accrued = add_bonus_points(accrual)
    if enote_accrued:
        accrual.accrued = True
        accrual.save()


@app.task
def process_not_accrued_bonuses():
    bonuses = BonusAccrual.objects.filter(accrued=False)
    for bonus in bonuses:
        accrual_bonuses_by_enote.delay(bonus.id)
