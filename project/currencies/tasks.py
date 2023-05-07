from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from currencies.clients.btc_trade_com_ua import doge_in_uah_client
from currencies.clients.bank_gov_ua import world_ccy_to_uah_client
from currencies.models import Currency
from project.celery import app


@shared_task
def get_currencies_task():
    doge_in_uah_client.save()
    world_ccy_to_uah_client.save()
