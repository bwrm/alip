from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/(?P<slug>[-\w]+)$', views.CreateReview.as_view(), name='create'),
    url(r'^list/(?P<slug>[-\w]+)$', views.ReviewListView.as_view(), name='list'),
]
