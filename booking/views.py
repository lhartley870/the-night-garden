import random
from django.shortcuts import render
from django.views import View
from .forms import BookingForm
from .models import Table


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
        """
        Method to evaluate multiple tables available for the booking.

        Finds any tables which are 'match' tables, being those that are the
        same size as the party_size (for even party sizes) and those that are
        the same size as the party_size + 1 (for odd party sizes). If there is
        1 match table, that is returned. If there is more than 1 match table,
        one is selected at random and returned. If there are no match tables,
        the evaluate_no_match_tables method is called to provide the table(s).

        This method provides the selected tables to the select_tables method.
        """
        # Creates a list of all 'match' tables, being available_tables that are
        # the same size as the party_size (for even party sizes) or the
        # party_size + 1 (for odd party sizes).
        match_tables = [
            table for table in available_tables
            if table.size == party_size or table.size == party_size + 1
        ]

        # If there is 1 match table, that is returned.
        if len(match_tables) == 1:
            allocated_tables = match_tables
        # If there is more than 1 match table, one is selected at random
        # and returned.
        elif len(match_tables) > 1:
            allocated_tables = [random.choice(match_tables)]
        # If there are no match tables, another method is called.
        else:
            allocated_tables = []

        return allocated_tables

    def select_tables(self, booking_form):
        """
        Method to select the table(s) for the booking.

        Gets all tables assigned to the chosen time_slot and removes any
        that have already been booked on the same date and for the same
        time slot. If only 1 table is available, that is returned. If more
        than 1 table is available, the evaluate_multiple tables method is
        called to return the table(s). In the unlikely event that no tables
        are available, 'None' is returned.

        This method provides the selected tables to the post method.
        """
        time_slot = booking_form.cleaned_data['time_slot']
        date = booking_form.cleaned_data['date']
        party_size = booking_form.cleaned_data['party_size']
        bookings = booking_form.get_current_bookings(date, time_slot)

        # Gets all the tables assigned to the chosen time slot and
        # removes any tables that have already been booked on the same date
        # and for that same time slot.
        available_tables = Table.objects.filter(
            table_timeslots=time_slot
        ).exclude(
            table_booking__in=bookings
        )

        # If there is only 1 available table, that is returned.
        if len(available_tables) == 1:
            allocated_tables = available_tables
        # If there is more than 1 available table, the
        # evaluate_multiple_tables method is called.
        elif len(available_tables) > 1:
            allocated_tables = self.evaluate_multiple_tables(available_tables,
                                                             party_size)
        # There should be tables available due to the validation carried out
        # prior to reaching this point but in the unlikely event that no tables
        # are available, 'None' is returned.
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
