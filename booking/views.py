from django.shortcuts import render
from django.views import View
from .forms import BookingForm
from .models import Table
import random


# Create your views here.
class HomePage(View):
    def get(self, request):
        return render(request, "index.html",)


class BookingFormPage(View):
    def get(self, request):
        return render(
            request,
            "booking_form.html",
            {
                "booking_form": BookingForm(),
            }
        )

    def evaluate_multiple_tables(self, available_tables, party_size):
        match_tables = [
            table for table in available_tables
            if table.size == party_size or table.size == party_size + 1
        ]
        print(match_tables)
        if len(match_tables) == 1:
            allocated_tables = match_tables[0]
        elif len(match_tables) > 1:
            allocated_tables = random.choice(match_tables)
        else:
            allocated_tables = []

        return allocated_tables

    def select_tables(self, booking_form):
        time_slot = booking_form.cleaned_data['time_slot']
        date = booking_form.cleaned_data['date']
        party_size = booking_form.cleaned_data['party_size']
        bookings = booking_form.get_current_bookings(date, time_slot)

        available_tables = Table.objects.filter(
            table_timeslots=time_slot
        ).exclude(
            table_booking__in=bookings
        )

        if len(available_tables) == 1:
            allocated_tables = available_tables[0]
        elif len(available_tables) > 1:
            allocated_tables = self.evaluate_multiple_tables(available_tables,
                                                             party_size)
        else:
            allocated_tables = None

        return allocated_tables

    def post(self, request, *args, **kwargs):

        booking_form = BookingForm(data=request.POST)

        if booking_form.is_valid():
            allocated_tables = self.select_tables(booking_form)

        return render(
            request,
            "booking_form.html",
            {
                 "booking_form": booking_form,
            }
        )
