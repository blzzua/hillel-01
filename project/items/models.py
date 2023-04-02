import uuid

from django.contrib.auth import get_user_model
from django.db import models
from os import path


User = get_user_model()
MIN_PRICE = 0.1


def upload_to(instance, filename):
    _name, extenstion = path.splitext(filename)
    return str(f'products/images/{str(instance.pk)}{extenstion}')


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(null=True, upload_to='images/items/{id}/image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_categories_names(self):
        return self.name

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    caption = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(null=True, upload_to='images/items/{id}/image')
    price = models.DecimalField(max_digits=18, decimal_places=2)
    sku = models.CharField(max_length=128)
    categories = models.ManyToManyField(Category, related_name='category', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.caption} [{self.sku}]'


class Discount(models.Model):
    class DiscountType(models.IntegerChoices):
        PCT = 0, 'percentage'
        ABS = 1, 'absolute'

    code = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    discount_type = models.PositiveSmallIntegerField(choices=DiscountType.choices, default=DiscountType.ABS)
    amount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate(self, price):
        if not self.is_active:
            return price
        else:
            if self.discount_type == Discount.DiscountType.ABS.value:
                return max(MIN_PRICE, price - self.amount)
            if self.discount_type == Discount.DiscountType.PCT.value:
                return max(MIN_PRICE, price * (100 - self.amount) / 100)
            print(f'Im here. because {self.discount_type=} {Discount.DiscountType.PCT.value=} {Discount.DiscountType.ABS.value=}')


class Order(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # user_name = models.CharField(max_length=255, null=True, on_delete=models.SET_NULL)
    user_name = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    order_number = models.IntegerField()
    total_price = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_name', 'order_number')

    def calculate_total_price(self):
        total_price = 0
        for item in OrderItem.objects.filter(order_id=self).all():
            total_price += item.discount_price
        return total_price

    def calculate_total_price2(self):
        total_price = 0
        for item in self.order_items.iterator():
            total_price += item.discount_price
        return total_price

    def save(self, *args, **kwargs):
        # donot  check if
        # if OrderItem.objects.filter(order_id=self, updated_at__gte=self.updated_at):
        self.total_price = self.calculate_total_price()
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    is_active = models.BooleanField(default=False)
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='order_items', )
    item_id = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    discount_id = models.ForeignKey(Discount, on_delete=models.DO_NOTHING)
    item_price = models.DecimalField(max_digits=18, decimal_places=2)
    quantity = models.SmallIntegerField(default=1)  # TODO: add checks, positive > 0.
    discount_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.discount_price = self.calculate_price_with_discount()
        super(OrderItem, self).save(*args, **kwargs)

    def calculate_price_with_discount(self):
        return self.discount_id.calculate(self.item_price * self.quantity)
