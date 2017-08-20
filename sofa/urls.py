from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SofaView.as_view(), name='sofa'),
]