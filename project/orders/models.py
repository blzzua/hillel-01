import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from items.models import Item, Discount
from django.utils.safestring import mark_safe

User = get_user_model()
MIN_PRICE = 0.1


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

    # def save(self, *args, **kwargs):
    #     # donot  check if
    #     # if OrderItem.objects.filter(order_id=self, updated_at__gte=self.updated_at):
    #     self.total_price = self.calculate_total_price()
    #     super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    is_active = models.BooleanField(default=False)
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='order_items', )
    item_id = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    discount_id = models.ForeignKey(Discount, on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    item_price = models.DecimalField(max_digits=18, decimal_places=2)
    quantity = models.SmallIntegerField(default=1)  # TODO: add checks, positive > 0.
    discount_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.discount_price = self.item_price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)
    #
    # def calculate_price_with_discount(self):
    #     return self.discount_id.calculate(self.item_price * self.quantity)
