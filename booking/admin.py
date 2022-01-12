from django.contrib import admin
from .models import Table


# Register your models here.
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):

    list_display = ('name', 'size')
    list_filter = ('name', 'size')
    search_fields = ['name', 'size']
