import random
import math
import itertools
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .forms import BookingForm
from .models import Table, Booking


# Create your views here.
class TableSelectionMixin:
    def filter_non_match_tables(self, combinations_capacities_dictionary,
                                combinations_num_tables_dictionary,
                                party_size):
        """
        Method to evaluate 'non match' table combinations.

        Where there are multiple available_tables all smaller in size than
        the party_size, not all the tables are needed to cover the
        party_size, there are more than 2 tables, not all the tables
        are the same size, and there is no 'match' combination of
        tables, this method gets the best 'non match' combination of
        tables. A 'match' here being a table combination capacity which is the
        same size as the party_size (for even party sizes) or the same size
        as the party_size + 1 (for odd party sizes).

        Where there are multiple available_tables, no one table or combination
        of tables is a 'match' and some of the tables are smaller in size
        than the party_size and some are larger in size than the party_size,
        this method gets the best 'non match' table or combination of tables.

        This method may be called upon to provide the selected table(s) to the
        combine_tables method.
        """
        # Creates a list of all the table combinations which have a smaller
        # seating capacity than the party_size.
        insufficient_combos = []
        for key, value in combinations_capacities_dictionary.items():
            if value < party_size:
                insufficient_combos.append(key)

        # Removes the table combinations which have a smaller seating capacity
        # than the party_size from the combo:capacity dictionary and the
        # combo:number of tables dictionary.
        for combo in insufficient_combos:
            del combinations_capacities_dictionary[combo]
            del combinations_num_tables_dictionary[combo]

        # Creates a list of the seating capacities covered by each of the
        # remaining table combinations and finds the smallest capacity that
        # is bigger than the party_size (the smallest viable capacity).
        capacities_bigger_party_size = list(
            combinations_capacities_dictionary.values())
        smallest_capacity_bigger_party_size = min(capacities_bigger_party_size)

        # Creates a list of the table combinations with a capacity bigger than
        # the smallest viable capacity.
        largest_combos = []
        for key, value in combinations_capacities_dictionary.items():
            if value != smallest_capacity_bigger_party_size:
                largest_combos.append(key)

        # Removes the table combinations with a capacity bigger than the
        # smallest viable capacity from the combo:capacity and combo:number
        # of tables dictionaries.
        for combo in largest_combos:
            del combinations_capacities_dictionary[combo]
            del combinations_num_tables_dictionary[combo]

        # If there is only 1 table combination remaining, that is returned.
        if len(combinations_capacities_dictionary) == 1:
            allocated_tables = list(
                combinations_capacities_dictionary.keys())[0]
        # If there is more than 1 table combination.
        else:
            # Finds the smallest number of tables in the remaining
            # table combinations.
            smallest_num_tables = min(list(
                combinations_num_tables_dictionary.values()))

            # Creates a list of the remaining table combinations which
            # have the smallest number of tables.
            smallest_num_tables_combos = []
            for key, value in combinations_num_tables_dictionary.items():
                if value == smallest_num_tables:
                    smallest_num_tables_combos.append(key)

            # If there is more than 1 remaining table combination with the
            # smallest number of tables, one will be selected at random and
            # returned. If there is only 1 combination left, that will be
            # returned.
            allocated_tables = random.choice(smallest_num_tables_combos)

        return allocated_tables

    def filter_match_tables(self, combinations_capacities_dictionary,
                            combinations_num_tables_dictionary,
                            match_table):
        """
        Method to evaluate 'match' table combinations.

        Where there are multiple available_tables all smaller in size than
        the party_size, not all the tables are needed to cover the
        party_size, there are more than 2 tables, not all the tables
        are the same size, and there is at least 1 'match' combination of
        tables, this method gets the best (or only) 'match' combination of
        tables. A 'match' here being a table combination capacity which is the
        same size as the party_size (for even party sizes) or the same size
        as the party_size + 1 (for odd party sizes).

        Where there are multiple available_tables, no one table is a 'match',
        some of the tables are smaller in size than the party_size and some
        are larger in size than the party_size, and there is at least 1 'match'
        combination of tables, this method gets the best (or only) 'match'
        combination of tables.

        This method may be called upon to provide the selected tables to the
        combine_tables method.
        """
        # Creates a list of all table combination tuples that 'match' the
        # party_size.
        match_keys = []
        for key, value in combinations_capacities_dictionary.items():
            if value == match_table:
                match_keys.append(key)

        # If there is only 1 table combination that is a 'match' return it.
        if len(match_keys) == 1:
            allocated_tables = match_keys[0]
        # If there is more than 1 table combination that is a 'match'.
        else:
            # Finds the smallest number of tables for a 'matching' table
            # combination.
            smallest_match_combo = min(
                [len(match_key) for match_key in match_keys]
            )

            # Creates a list of all the 'matching' table combinations which
            # have the smallest number of tables.
            smallest_match_keys = []
            for key, value in combinations_num_tables_dictionary.items():
                if key in match_keys and value == smallest_match_combo:
                    smallest_match_keys.append(key)

            # If there is only 1 'matching' table combination with the
            # smallest number of tables, return that.
            if len(smallest_match_keys) == 1:
                allocated_tables = smallest_match_keys[0]
            # If there is more than 1 'matching' table combination with the
            # smallest number of tables.
            else:
                # Creates a list of all the table sizes for all the tables in
                # the 'matching' table combinations with the smallest number of
                # tables and finds the largest table size from that list.
                tables_sizes = []
                for match_key in smallest_match_keys:
                    for table in match_key:
                        tables_sizes.append(table.size)
                largest_table_size = max(tables_sizes)

                # Creates a list of all the tables with the largest_table_size
                # found within the 'matching' table combinations with the
                # smallest number of tables.
                big_tables = []
                for smallest_match_key in smallest_match_keys:
                    for table in smallest_match_key:
                        if table.size == largest_table_size:
                            big_tables.append(table)

                # Removes any duplicates from the list of big_tables.
                # The code to remove duplicates from a list was adapated
                # from a W3 Schools article entitled 'How to Remove
                # Duplicates From a Python List' found at this link -
                # https://www.w3schools.com/python/python_howto_remove_duplicates.asp
                big_tables = list(dict.fromkeys(big_tables))

                # Filters the list of 'matching' table combinations with the
                # smallest number of tables to those combinations that also
                # contain a table in the big_tables list. Creates a new
                # best_combos list.
                best_combos = []
                for big_table in big_tables:
                    for smallest_match_key in smallest_match_keys:
                        if big_table in smallest_match_key:
                            best_combos.append(smallest_match_key)

                # If there is only 1 table combination in the best_combos list
                # return that.
                if len(best_combos) == 1:
                    allocated_tables = best_combos[0]
                # If there is more than 1 table combination in the best_combos
                # list, select one of the combinations at random and return
                # that.
                else:
                    allocated_tables = random.choice(best_combos)

        return allocated_tables

    def combine_tables(self, available_tables, party_size, min_combo_size):
        """
        Method to evaluate table combinations.

        Where there are multiple available_tables all smaller in size than
        the party_size, not all the tables are needed to cover the
        party_size, there are more than 2 tables and not all the tables
        are the same size, this method gets the best combination of tables.

        Where there are multiple available_tables, no one table is a 'match'
        (a 'match' being a size which is the same size as the party_size
        (for even party sizes) or the same size as the party_size + 1
        (for odd party sizes)) and some of the tables are smaller in size than
        the party_size and some are larger in size than the party_size, this
        method gets the best table or combination of tables.

        This method may be called upon to provide the selected table(s) to the
        evaluate_smaller_tables method or the evaluate_no_match_tables method.
        """
        # Creates a list of table combination tuples where the minimum
        # combination size is as per the min_combo_size specified.
        combinations = []
        # Code for creating a list of all possible table combinations for a
        # particular minimum combination size and above was
        # adapted from a response provided by Dan H and edited by Steven C.
        # Howell on this Stack Overflow post -
        # https://stackoverflow.com/questions/464864/how-to-get-all-possible
        # -combinations-of-a-list-s-elements
        for length in range(min_combo_size, len(available_tables) + 1):
            for subset in itertools.combinations(available_tables, length):
                combinations.append(subset)

        # Creates a list of the number of tables in each combination.
        combinations_num_tables = [
            len(combination) for combination in combinations
        ]

        # Creates a list of the seating capacity for each combination.
        combinations_capacities = []
        for combination in combinations:
            combination_capacity = sum([table.size for table in combination])
            combinations_capacities.append(combination_capacity)

        # Creates a combo:capacities dictionary where a table combination
        # tuple is the key and the seating capacity of that tuple is the value.
        # Code for creating a dictionary from two lists was adapted from an
        # answer given by Dan Lenski and edited by wjandrea on this Stack
        # Overflow post -
        # https://stackoverflow.com/questions/209840/how-do-i-convert-two-lists-
        # into-a-dictionary
        combinations_capacities_dictionary = dict(zip(combinations,
                                                  combinations_capacities))
        # Creates a combo:number of tables dictionary where a table combination
        # tuple is the key and the number of tables in that tuple is the value.
        combinations_num_tables_dictionary = dict(zip(combinations,
                                                  combinations_num_tables))

        match_table = None
        # If the party_size is even, set match_table to that value.
        if party_size % 2 == 0:
            match_table = party_size
        # If the party_size is odd, set match_table to that value + 1.
        else:
            match_table = party_size + 1

        # A different method is called depending on whether there is
        # a 'matching' table combination or not.
        if match_table in combinations_capacities:
            allocated_tables = self.filter_match_tables(
                combinations_capacities_dictionary,
                combinations_num_tables_dictionary,
                match_table)
        else:
            allocated_tables = self.filter_non_match_tables(
                combinations_capacities_dictionary,
                combinations_num_tables_dictionary,
                party_size)

        return allocated_tables

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

        This method may be called upon to provide the selected tables to the
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
            allocated_tables = self.combine_tables(available_tables,
                                                   party_size,
                                                   min_combo_size)

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

        This method may be called upon to provide the selected tables to the
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
            allocated_tables = self.combine_tables(available_tables,
                                                   party_size,
                                                   min_combo_size)

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

        This method may be called upon to provide the selected tables to the
        select_tables method.
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

    def select_tables(self, available_tables, party_size):
        """
        Method to select the table(s) for the booking.

        Evaluates the available_tables. If only 1 table is available,
        that is returned. If more than 1 table is available, the
        evaluate_multiple tables method is called to return the table(s).
        In the unlikely event that no tables are available, 'None' is returned.

        This method provides the selected tables to the get_allocated_tables
        method.
        """
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

    def get_allocated_tables(self, booking_form, edit, *args):
        """
        Method to get the allocated table(s) for the booking.

        Gets all tables assigned to the chosen time_slot and removes any
        that have already been booked on the same date and for the same
        time slot (save for any tables allocated to an existing booking being
        edited where the existing booking has the same date and time_slot
        as the edited booking). This method provides the available_tables
        to the select_tables method and gets the final allocated table(s)
        for the booking back.

        This method provides the allocated tables to the post method.
        """
        time_slot = booking_form.cleaned_data['time_slot']
        date = booking_form.cleaned_data['date']
        party_size = booking_form.cleaned_data['party_size']

        # If edit is true then an existing booking is being edited
        # where the existing booking has the same date and time_slot
        # as the edited booking. Therefore the table(s) allocated
        # to the existing booking need to be made available to the
        # available_tables variable.
        if edit:
            bookings = booking_form.get_current_bookings(
                date, time_slot
            ).exclude(
                id=args[0]
            )
        else:
            bookings = booking_form.get_current_bookings(date, time_slot)

        # Gets all the tables assigned to the chosen time slot and
        # removes any tables that have already been booked on the same date
        # and for that same time slot (apart from an existing booking that
        # is being edited with the same date and time_slot which will have been
        # excluded from the bookings variable above).
        available_tables = Table.objects.filter(
            table_timeslots=time_slot
        ).exclude(
            table_booking__in=bookings
        )

        allocated_tables = self.select_tables(available_tables, party_size)

        return allocated_tables


class HomePage(View):
    def get(self, request):
        return render(request, "index.html",)


class MyBookingsPg(View):
    # The solution of using the @cache_control decorator to control what
    # happens if a user logs out of their account and then presses the
    # back button was taken from an answer given by Mahmood on this Stack
    # Overflow post -
    # https://stackoverflow.com/questions/28000981/django-user-re-entering
    # -session-by-clicking-browser-back-button-after-logging?noredirect=1&lq=1
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        # Filters the bookings so that only those of the logged in user
        # are displayed, excludes bookings for dates before today
        # and excludes any bookings for today before the current time.
        bookings = Booking.objects.filter(
            booker=request.user
        ).exclude(
            date__lt=current_date
        ).exclude(
            date=current_date,
            time_slot__time__lt=current_time
        )
        return render(
            request,
            "my_bookings.html",
            {
                "bookings": bookings
            })


class BookingFormPage(View, TableSelectionMixin):
    # The solution of using the @cache_control decorator to control what
    # happens if a user logs out of their account and then presses the
    # back button was taken from an answer given by Mahmood on this Stack
    # Overflow post -
    # https://stackoverflow.com/questions/28000981/django-user-re-entering
    # -session-by-clicking-browser-back-button-after-logging?noredirect=1&lq=1
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        # Code for providing an initial value in a model form field
        # was adapted from code provided in an article entitled 'Django
        # Initial Value to Model forms' by challapallimanoj99@gmail.com
        # dated 16 June 2021 and found at this link -
        # https://studygyaan.com/django/how-to-give-initial-value-to-model-forms
        current_date = datetime.now().date()
        # The booking form will have today's date initially inserted as
        # the date value.
        initial_data = {
            'date': current_date
        }
        booking_form = BookingForm(initial=initial_data)
        return render(
            request,
            "booking_form.html",
            {
                "booking_form": booking_form,
            }
        )

    def post(self, request, *args, **kwargs):
        booking_form = BookingForm(data=request.POST)

        if booking_form.is_valid():
            edit = False
            allocated_tables = self.get_allocated_tables(booking_form, edit)
            # There should be tables available due to the validation carried
            # out prior to reaching this point but in the unlikely event that
            # no tables are available when the select_tables method is run,
            # an appopriate message is returned to the user.
            if allocated_tables is None:
                messages.error(request,
                               'Sorry this booking is no longer available')
            else:
                booking = booking_form.save(commit=False)
                booking.booker = request.user
                booking.save()
                # If there is only 1 allocated_table, that is added to the
                # booking.
                if len(allocated_tables) == 1:
                    booking.tables.add(allocated_tables[0].id)
                # If there are multiple allocated tables, they are added to the
                # booking.
                else:
                    for table in allocated_tables:
                        booking.tables.add(table.id)

                # HttpResponseRedirect returned after successfully dealing
                # with POST data as recommended by the Django documentation as
                # this prevents data from being posted twice if a user hits
                # the back button - described in an example on this page -
                # https://docs.djangoproject.com/en/4.0/intro/tutorial04/.
                # The redirect shortcut function returns an
                # HttpResponseRedirect to the appropriate url for the
                # arguments passed.
                return redirect('my_bookings')

        return render(
            request,
            "booking_form.html",
            {
                 "booking_form": booking_form,
            }
        )


class EditBookingPage(View):
    # The solution of using the @cache_control decorator to control what
    # happens if a user logs out of their account and then presses the
    # back button was taken from an answer given by Mahmood on this Stack
    # Overflow post -
    # https://stackoverflow.com/questions/28000981/django-user-re-entering
    # -session-by-clicking-browser-back-button-after-logging?noredirect=1&lq=1
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking_form = BookingForm(instance=booking)
        return render(
            request,
            "edit_booking.html",
            {
                "booking_form": booking_form,
            }
        )
