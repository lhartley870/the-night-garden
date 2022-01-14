from django.contrib import admin
from .models import Table, TimeSlot
from .forms import TimeSlotForm


# Register your models here.
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):

    list_display = ('name', 'size')
    list_filter = ('name', 'size')
    search_fields = ['name', 'size']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):

    form = TimeSlotForm

    list_display = ('booking_time', 'allocated_tables')
    list_filter = ('time', 'tables')
    search_fields = ['time', 'tables__name']

    def booking_time(self, obj):
        """
        Method to display each time slot in the Admin panel
        in the 24 hour clock format rather than the default '5:30 p.m.' format
        for consistency with the database and the search field.
        """
        twenty_four_hour_clock_time = obj.time.strftime("%H:%M")
        return twenty_four_hour_clock_time

    def allocated_tables(self, obj):
        """
        Method to enable the name and size of each table allocated to a
        time slot to be displayed in the Admin panel list of time slots as
        Many to Many fields are not supported in list_display.
        """
        # Code for the display of each time slot's table details was adapted
        # from an answer given by  karthikr and edited by Joseph jun.
        # Melettukunnel on this Stack Overflow post -
        # https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
        return ", ".join([f'{table.name} ({table.size})'
                         for table in obj.tables.all()])
