from django.contrib import admin
from .models import Table, TimeSlot, Booking
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


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, TablesMixin):

    filter_vertical = ('tables',)
    list_display = ('id', 'booking_date', 'time_slot', 'party_size',
                    'allocated_tables', 'booker', 'approved',
                    'created_on')
    list_filter = ('date', 'time_slot', 'party_size',
                   'tables', 'booker', 'approved')
    search_fields = ['date']

    def booking_date(self, obj):
        """
        Method to display each booking date in the Admin panel
        in the '2022-01-03' format rather than the default 'Jan. 03, 2022'
        format for consistency with the search field format, the format of the
        date field in the admin form for bookings and the database.
        """
        year_month_date_format = obj.date.strftime("%Y-%m-%d")
        return year_month_date_format
