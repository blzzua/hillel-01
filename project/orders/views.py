from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404
from django.core.exceptions import ObjectDoesNotExist

from items.models import Item
from orders.models import Order, OrderItem

class OrderItemView(View):
    def get(self, request):
        # form = OrderCountView()
        user = request.user
        order, is_created = Order.objects.get_or_create(user_name=user, is_active=True, defaults={'order_number': 1, 'is_active': True, 'is_paid': False, 'is_active':True})
        if is_created:
            prev_order = Order.objects.filter(user_name=user).order_by('-order_number').first()
            if prev_order:
                order.order_number = prev_order.order_number + 1
                order.save()

        try:
            item_id = request.GET.get('item')
            item = Item.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            # redirect 404
            raise Http404(f"Товар {item_id} незнайдений")


        context = {'item': item, 'order': order}
        return render(request, 'order/add.html', context=context)

    def post(self, request):  # feedback_index
        post_data = request.POST
        order_number = post_data.get('order_number')
        quantity = post_data.get('quantity')
        item_id = post_data.get('item')
        item = Item.objects.get(id=item_id)
        user = request.user
        order = Order.objects.get(user_name=user, is_active=True, order_number=order_number)
        order

        context = {'item': item, 'order': order}
        order_item = OrderItem.objects.create(
            is_active=True,
            order_id=order,
            item_id=item,
            discount_id=None,
            item_price=item.price,
            quantity=quantity,
            discount_price=item.price
        )

        return redirect(reverse('add_orderitem'), kwargs={'item': item_id})



class OrderDetailView(View):
    def get(self, request):
        user = request.user
        order, is_created = Order.objects.get_or_create(user_name=user, is_active=True, defaults={'order_number': 1, 'is_active': True, 'is_paid': False, 'is_active':True})
        if is_created:
            prev_order = Order.objects.filter(user_name=user).order_by('-order_number').first()
            if prev_order:
                order.order_number = prev_order.order_number + 1
                order.save()

        orderitems = [item for item in order.order_items.all()]
        context = {'order': order, 'orderitems': orderitems}

        return render(request, 'order/detail.html', context=context)
