from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^photo-upload/$', views.PhotoUploadView.as_view(), name='photo_upload'),
    url(r'^file-upload/$', views.FilesUploadView.as_view(), name='files_upload'),
    url(r'^deletefile/$', views.deletemyfile, name='delete_file'),
    url(r'^finishcreating/$', views.uploadsave, name='finish-creating'),
]
