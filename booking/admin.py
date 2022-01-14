from django.contrib import admin
from .models import Table, TimeSlot


# Register your models here.
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):

    list_display = ('name', 'size')
    list_filter = ('name', 'size')
    search_fields = ['name', 'size']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):

    list_display = ('time',)
    list_filter = ('time', 'tables')
    search_fields = ['time', 'tables__name']
