from django.contrib import admin
from .models import *

# # Register your models here.
# admin.site.register('Category')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','tenant_id',)
    search_fields = ['id','name','tenant_id__name']

admin.site.register(Categorys,CategoryAdmin)