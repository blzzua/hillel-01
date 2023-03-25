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
    #image = models.ImageField(null=True, upload_to='images/items/{id}/image')
    sku = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)