
from django.urls import path
from orders.views import OrderItemView, OrderDetailView

urlpatterns = [
    path('add', OrderItemView.as_view(), name='add_orderitem'),
    path('detail', OrderDetailView.as_view(), name='order_detail'),
]