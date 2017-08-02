from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ParcerView.as_view(), name='parcer'),
    # url(r'^orders/$', views.OrderList.as_view(), name='orders'),
    url(r'^orders-ajax/$', views.OrderAjax, name='orders-ajax'),
    url(r'^invoce/$', views.invoce_view, name='invoce'),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetail.as_view(), name='order-detail'),
    url(r'^add-to-list/$', views.add_to_shopping_list_view, name='add_to_list'),
]