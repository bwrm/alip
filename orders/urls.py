from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^myoders/$', views.MyOrders.as_view(), name='my_orders'),
]
