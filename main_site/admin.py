from django.contrib import admin
from .models import Product, Category, Delivery, OurProfit
from django.template.defaultfilters import slugify

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}
# admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'designer_price', 'available', 'created', 'updated']
    list_filter = ['category', 'designer_price', 'available', 'created', 'updated']
    list_editable = ['available']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Product, ProductAdmin)

admin.site.register(Delivery)
admin.site.register(OurProfit)

