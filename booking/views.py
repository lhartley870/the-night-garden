import random
import math
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

    def evaluate_smaller_tables(self, available_tables, party_size):
        """
        Method to evaluate multiple tables smaller than the party_size.

        Where there are multiple available_tables smaller in size than
        the party_size, if the combined capacity of all the available_tables
        is a 'match' for the party_size (a 'match' being a capacity which
        is the same size as the party_size (for even party sizes) or the
        same size as the party_size + 1 (for odd party sizes)), or there
        are only 2 available tables, all the available_tables are returned.
        Alternatively, if all the tables are the same size but there are more
        than 2 and not all the tables are needed for a 'match', the smallest
        number of those tables required to cover the party_size is returned.
        If neither of those options applies, the combine_tables method is
        called to provide the table(s).

        This method provides the selected tables to the
        evaluate_no_match_tables method.
        """
        # Creates a list of the size of each available_table.
        table_sizes = [table.size for table in available_tables]
        # Gets the number of available_tables.
        num_available_tables = len(available_tables)

        # If the combined capacity of all the available_tables is
        # a 'match' for the party_size or there are only 2
        # available_tables, all available_tables are returned.
        if (sum(table_sizes) == party_size
            or sum(table_sizes) == party_size + 1
                or num_available_tables == 2):
            allocated_tables = available_tables
        # Else if all the tables are the same size, the minimum number of
        # those tables needed to cover the party_size is returned.
        elif (len(available_tables.filter(size=table_sizes[0]))
              == num_available_tables):
            number_tables_needed = math.ceil(party_size / table_sizes[0])
            allocated_tables = available_tables.all()[:number_tables_needed]
        # If neither of the above options apply, another method is called.
        else:
            min_combo_size = 2
            allocated_tables = []

        return allocated_tables

    def evaluate_no_match_tables(self, available_tables, party_size):
        """
        Method to evaluate multiple tables where there are no 'match' tables.

        Where there are multiple available_tables but none which are a 'match'
        for the party_size (a 'match' being a table which is the same size as
        the party_size (for even party sizes) or a table which is the same size
        as the party_size + 1 (for odd party sizes)), this method finds out
        whether all the available tables are smaller in size than the
        party_size, larger in size than the party_size or whether some
        available_tables are smaller and some are larger. If all tables are
        larger, the smallest of those tables is returned (or if there is more
        than 1, 1 of those tables chosen at random). If all the tables are
        smaller than the party_size, the evaluate_smaller_tables method is
        called to provide the table(s). If some tables are smaller and some
        are larger than the party_size, the combine_tables method is called
        to provide the table(s).

        This method provides the selected tables to the
        evaluate_multiple_tables method.
        """
        # Creates a list of all the available_tables with a smaller size
        # than the party_size.
        tables_smaller_than_party = [
            table for table in available_tables
            if table.size < party_size
        ]

        # If there are no tables in the tables_smaller_than_party list
        # then all available_tables must be larger than the party_size.
        # The smallest of the available_tables is chosen (or 1 of the
        # smallest is chosen at random if there is more than 1).
        if len(tables_smaller_than_party) == 0:
            table_sizes = [table.size for table in available_tables]
            smallest_table_size = min(table_sizes)
            smallest_tables = available_tables.filter(size=smallest_table_size)
            if len(smallest_tables) == 1:
                allocated_tables = smallest_tables
            else:
                allocated_tables = [random.choice(smallest_tables)]
        # If all the available_tables are smaller in size than the party_size
        # another method is called.
        elif len(tables_smaller_than_party) == len(available_tables):
            allocated_tables = self.evaluate_smaller_tables(available_tables,
                                                            party_size)
        # If some tables are smaller than the party_size and some are larger,
        # another method is called.
        else:
            min_combo_size = 1
            allocated_tables = []

        return allocated_tables

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
            allocated_tables = self.evaluate_no_match_tables(available_tables,
                                                             party_size)

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
