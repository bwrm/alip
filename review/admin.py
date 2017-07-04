from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating', 'item', 'is_published']
    list_editable = ['is_published',]
    list_filter = ['is_published', 'rating', 'author']
admin.site.register(Review, ReviewAdmin)
