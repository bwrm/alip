from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^myaccount/signin/$', views.login, name = 'login'),
    url(r'^myaccount/signout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'', include('main_site.urls')),
    url(r'^myaccount/', include('autoriz.urls', namespace='autoriz')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^review/', include('review.urls', namespace='review')),
    url(r'', include('upload.urls', namespace='upload')),
    url(r'^edg/', include('edg.urls', namespace='edg')),
    url(r'^sofa/', include('sofa.urls', namespace='sofa')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)