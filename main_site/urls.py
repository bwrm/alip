from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

app_name = 'main_site'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^products/(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$', views.ProdDetailView.as_view(), name='product'),
    #/products/category/
    url(r'^products/(?P<category>[-\w]+)/$', views.ProdCatView.as_view(), name='productcat'),
    url(r'^products/$', views.GoodListView.as_view(), name='products'),
    url(r'^test/$', views.sometest, name='test'),
    url(r'^product/add/$', views.ProductCreate.as_view(), name='product-add'),
    # url(r'^product/(?P<prod_cat>[a-zA-Z0-9]+)/(?P<pk>[0-9]+)/update$', views.ProductUpdate.as_view(), name='product-update'),
    url(r'^product/(?P<pk>[0-9]+)/update$', views.ProductUpdate.as_view(), name='product-update'),
    url(r'^product/(?P<pk>[0-9]+)/produce$', views.ProductProduce.as_view(), name='product-produce'),
    url(r'^product/(?P<pk>[0-9]+)/produce/settings$', views.ProductProduceSet.as_view(), name='product-produce-set'),
    url(r'^product/(?P<pk>[0-9]+)/cancel-produce$', views.CancelProduce.as_view(), name='cancel-produce'),
    #/product/cat/2/update
    url(r'^product/(?P<pk>[0-9]+)/delete$', views.ProductDelete.as_view(), name='product-del'),
    #/product/cat/2/delete
    url(r'^about/$', TemplateView.as_view(template_name='./main_site/about.html'), name='about'),
    url(r'^map/$', views.ProducerListView.as_view(), name='map'),
]