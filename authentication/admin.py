from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','staffid','first_name','last_name','tenant_id')
    search_fields = ['id','staffid','tenant_id__name']

admin.site.register(User,UserAdmin)


