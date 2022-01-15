from django.contrib import admin
from .models import Table, TimeSlot
from .forms import TimeSlotForm


class TablesMixin:
    """
    Mixin to allow table details to be displayed in an Admin panel list_display
    where tables is a Many to Many field and so not supported in list_display.
    """
    def allocated_tables(self, obj):
        """
        Method to enable the name and size of each allocated table to be
        displayed in an Admin panel list.
        """
        # Code for the display of each table's details was adapted
        # from an answer given by  karthikr and edited by Joseph jun.
        # Melettukunnel on this Stack Overflow post -
        # https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
        return ", ".join(
            [
                f'{table.name} ({table.size})'
                for table in obj.tables.all()
            ]
        )


# Register your models here.
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):

    list_display = ('name', 'size')
    list_filter = ('name', 'size')
    search_fields = ['name', 'size']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin, TablesMixin):

    form = TimeSlotForm

    filter_vertical = ('tables',)
    list_display = ('booking_time', 'allocated_tables')
    list_filter = ('time', 'tables')
    search_fields = ['time', 'tables__name']

    def booking_time(self, obj):
        """
        Method to display each time slot in the Admin panel
        in the 24 hour clock format rather than the default '5:30 p.m.' format
        for consistency with the database and the search field format.
        """
        twenty_four_hour_clock_time = obj.time.strftime("%H:%M")
        return twenty_four_hour_clock_time
