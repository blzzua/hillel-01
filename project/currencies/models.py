from django.db import models
import uuid

from project.constants import MAX_DIGITS

from project.model_choices import Currencies


class Currency(models.Model):
    code = models.CharField(primary_key=True, max_length=16, choices=Currencies.choices,  default=Currencies.COIN)
    amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=8, default=1)
    units = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.amount}"


class CurrencyHistory(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    code = models.CharField(max_length=16, choices=Currencies.choices)
    amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=8)
    units = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.amount}"
