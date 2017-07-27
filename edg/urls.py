from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ParcerView.as_view(), name='parcer'),
]