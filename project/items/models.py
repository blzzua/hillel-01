import uuid


from django.db import models
from os import path


# Create your models here.
def upload_to(instance, filename):
    _name,  extenstion = path.splitext(filename)
    return str(f'products/images/{str(instance.pk)}{extenstion}')


class Item(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    caption = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(null=True, upload_to='images/items/{id}/image')
    sku = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, upload_to='images/items/{id}/image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Discount(models.Model):
    class DiscountType(models.IntegerChoices):
        PCT = 0, 'percentage'
        ABS = 1, 'absolute'

    code = models.CharField(max_length=30),
    description = models.TextField(blank=True, null=True)
    discount_type = models.PositiveSmallIntegerField(choices=DiscountType, default=DiscountType.ABS)
    amount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
