
from django.urls import path
from orders.views import OrderItemView, OrderDetailView, OrderItemDetailView, OrderItemDeletelView

urlpatterns = [
    path('add', OrderItemView.as_view(), name='add_orderitem'),
    path('detail', OrderDetailView.as_view(), name='order_detail'),
    path('item/<uuid:orderitem_id>/detail', OrderItemDetailView.as_view(), name='order_item_detail'),
    path('item/<uuid:orderitem_id>/delete', OrderItemDeletelView.as_view(), name='order_item_delete'),
]