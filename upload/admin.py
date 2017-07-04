from django.contrib import admin
from .models import Photo, Files

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['file', 'title', 'product']
    list_filter = ['product',]
admin.site.register(Photo, PhotoAdmin)