from django.contrib import admin
from .models import MyUser, Producer

# Re-register UserAdmin
admin.site.register(MyUser)
admin.site.register(Producer)