from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.register, name='register'),
    #/myaccount/
    # url(r'^myaccount/$', views.MyAccountView.as_view(), name='myaccount-home'),
    url(r'^$', views.PlainUser.as_view(), name='myaccount-home'),
    # url(r'^myaccount/add-service$', views.TypeService.as_view(), name='add-service'),
    # url(r'^myaccount/CNC$', views.CncReg.as_view(), name='cnc-service'),
    # url(r'^myaccount/plainuser$', views.PlainUser.as_view(), name='plainuser-profile'),
    url(r'^myproducts$', views.AllUsersProduct.as_view(), name='users-products'),
    url(r'^produced-by-me$', views.ProductsProducedByMe.as_view(), name='produced-products'),
    url(r'^myaccount/newproducer$', views.ProducerReg.as_view(), name='become-producer'),
]