from django.contrib import admin
from .models import Order

admin.site.site_header = 'Ikea\'s parcer'

from django.contrib.admin.views.main import ChangeList

class FooChangeList(ChangeList):
    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        return '/edg/orders/%d/' % (pk)




class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'price', 'is_paid', 'created_date']
    list_filter = ['is_paid', 'created_date']
    list_editable = ['is_paid']

    def get_changelist(self, request, **kwargs):
        return FooChangeList

    def has_add_permission(self, request):
        return False


admin.site.register(Order, OrderAdmin)
