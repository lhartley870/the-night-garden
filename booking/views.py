from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from .forms import BookingForm
from .models import Booking, TimeSlot
from .table_mixin import TableSelectionMixin


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, "index.html",)


class MyBookings(View):
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

        # Pagination code adapted from Django documentation.
        paginator = Paginator(bookings, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        booking_dates = [booking.date for booking in bookings]
        duplicate_booking_dates = [
            booking_date for booking_date in booking_dates
            if booking_dates.count(booking_date) > 1
        ]

        return render(
            request,
            "my_bookings.html",
            {
                "bookings": bookings,
                "page_obj": page_obj,
                "duplicate_booking_dates": duplicate_booking_dates,
            }
        )


class MakeBooking(View, TableSelectionMixin):
    # The solution of using the @cache_control decorator to control what
    # happens if a user logs out of their account and then presses the
    # back button was taken from an answer given by Mahmood on this Stack
    # Overflow post -
    # https://stackoverflow.com/questions/28000981/django-user-re-entering
    # -session-by-clicking-browser-back-button-after-logging?noredirect=1&lq=1
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request):
        # The booking form will have today's date initially inserted as
        # the date value unless today's date is a Monday or Tuesday (when
        # the restaurant is closed) or is during the Christmas shutdown.
        # If the former, the date initially inserted will be the next
        # Wednesday and if the latter, the date initially inserted will be
        # 04/01/2023.
        current_date = datetime.now().date()
        closed_day = current_date.weekday() == 0 or current_date.weekday() == 1
        christmas_closed_dates = [
            datetime(2022, 12, 24).date(),
            datetime(2022, 12, 25).date(),
            datetime(2022, 12, 28).date(),
            datetime(2022, 12, 29).date(),
            datetime(2022, 12, 30).date(),
            datetime(2022, 12, 31).date(),
            datetime(2023, 1, 1).date()
        ]

        if closed_day:
            if current_date.weekday() == 0:
                current_date = current_date + timedelta(days=2)
            else:
                current_date = current_date + timedelta(days=1)

        if current_date in christmas_closed_dates:
            current_date = datetime(2023, 1, 4).date()

        # Code for providing an initial value in a model form field
        # was adapted from code provided in an article entitled 'Django
        # Initial Value to Model forms' by challapallimanoj99@gmail.com
        # dated 16 June 2021 and found at this link -
        # https://studygyaan.com/django/how-to-give-initial-value-to-model-forms
        initial_data = {
            'date': current_date
        }
        booking_form = BookingForm(user=None, initial=initial_data)
        return render(
            request,
            "make_booking.html",
            {
                "booking_form": booking_form,
            }
        )

    def post(self, request, *args, **kwargs):
        booking_form = BookingForm(user=request.user, data=request.POST)

        if booking_form.is_valid():
            edit = False
            allocated_tables = self.get_allocated_tables(booking_form, edit)
            # There should be tables available due to the validation carried
            # out prior to reaching this point but in the unlikely event that
            # no tables are available when the get_allocated_tables method is
            # run, an appropriate message is returned to the user.
            if allocated_tables is None:
                messages.error(request,
                               'Sorry this booking is unavailable')
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

                created_booking = Booking.objects.filter(
                    booker=request.user
                ).order_by(
                    'created_on'
                ).last()
                # Use of .format() to add the booking details to
                # the success message taken from an answer given by
                # Glenn D.J. on this Stack Overflow post -
                # https://stackoverflow.com/questions/64956279/django-show-
                # message-only-when-form-has-changed
                messages.success(request,
                                 'Your {} has been '
                                 'submitted for approval'.format(
                                     created_booking))
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
            "make_booking.html",
            {
                 "booking_form": booking_form,
            }
        )


class EditBooking(View, TableSelectionMixin):
    # The solution of using the @cache_control decorator to control what
    # happens if a user logs out of their account and then presses the
    # back button was taken from an answer given by Mahmood on this Stack
    # Overflow post -
    # https://stackoverflow.com/questions/28000981/django-user-re-entering
    # -session-by-clicking-browser-back-button-after-logging?noredirect=1&lq=1
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking_form = BookingForm(user=None, instance=booking)
        return render(
            request,
            "edit_booking.html",
            {
                "booking_form": booking_form,
            }
        )

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking_form = BookingForm(user=request.user, data=request.POST,
                                   instance=booking)

        # If the user is editing a booking but only changing the party_size
        # i.e. the date and time_slot are not changing, edit needs to be set
        # to True so that the table(s) allocated to the original booking
        # will not be excluded when the get_allocated_tables method
        # creates a list of available_tables.
        time_slot_id = request.POST.get('time_slot')
        form_time_slot = TimeSlot.objects.get(id=time_slot_id)
        same_date = str(booking.date) == request.POST.get('date')
        same_time_slot = booking.time_slot == form_time_slot

        if same_date and same_time_slot:
            edit = True
        else:
            edit = False

        if booking_form.is_valid():
            allocated_tables = self.get_allocated_tables(booking_form,
                                                         edit, booking_id)
            # There should be tables available due to the validation carried
            # out prior to reaching this point but in the unlikely event that
            # no tables are available when the get_allocated_tables method is
            # run, an appropriate message is returned to the user.
            if allocated_tables is None:
                messages.error(request,
                               'Sorry this booking is unavailable')
            else:
                booking = booking_form.save(commit=False)
                booking.booker = request.user
                booking.approved = False
                # The table(s) allocated to the existing booking need to be
                # removed before the newly allocated table(s) are added.
                booking.tables.clear()
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

                edited_booking = get_object_or_404(Booking, id=booking_id)
                messages.success(request,
                                 'Your edited {} has been '
                                 'submitted for approval'.format(
                                     edited_booking))
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
            "edit_booking.html",
            {
                 "booking_form": booking_form,
            }
        )


class CancelBooking(View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        messages.success(request,
                         'Your {} has been '
                         'successfully cancelled'.format(booking))
        booking.delete()

        return redirect('my_bookings')


class Menus(View):
    def get(self, request):
        return render(request, "menus.html")


class ContactUs(View):
    def get(self, request):
        return render(request, "contact.html")
