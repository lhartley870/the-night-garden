from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms.widgets import Select
from django.shortcuts import get_object_or_404
from allauth.account.forms import SignupForm
from .models import TimeSlot, Booking


class TimeSlotForm(forms.ModelForm):

    class Meta:
        model = TimeSlot
        fields = ('time', 'tables')

    def clean_time(self):
        """
        Method to add validation when an Admin user is adding/editing time
        slots to ensure that slots are not added before the restaurant opens at
        17:30 or after 22:00 (to allow enough time between the last booking
        slot and the restaurant closing at midnight).
        """
        # Code for this method was adapted from a question posted by Amistad
        # and an answer given by Daniel Roseman on this Stack Overflow post -
        # https://stackoverflow.com/questions/24802244/custom-validation-in-django-admin
        time = self.cleaned_data.get('time')
        too_early = time.hour < 17 or time.hour == 17 and time.minute < 30
        too_late = time.hour > 22 or time.hour == 22 and time.minute > 00
        if (too_early or too_late):
            raise ValidationError('Time slots must be between 17:30 and 22:00')
        else:
            return self.cleaned_data['time']


class CustomSignUpForm(SignupForm):
    """
    CustomSignUpForm class added so that the django-allauth
    standard SignUpForm class can be extended to add first name and
    last name fields.
    """

    # Code for this CustomSignUpForm class is based upon code
    # included in an article entitled 'The complete django-allauth guide'
    # by Gajesh at -
    # https://dev.to/gajesh/the-complete-django-allauth-guide-la3
    #
    # Code for validating the first_name and last_name fields so that
    # only letters are allowed was adapted from an answer given by
    # Martijn Pieters and edited by Lord Elrond on this Stack Overflow
    # post - https://stackoverflow.com/questions/17165147/how-can-i-make-
    # a-django-form-field-contain-only-alphanumeric-characters
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')
    first_name = forms.CharField(max_length=30, label='First Name',
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'First Name'}),
                                 validators=[alpha])
    last_name = forms.CharField(max_length=30, label='Last Name',
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Last Name'}),
                                validators=[alpha])

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class BookingForm(forms.ModelForm):

    class Meta:
        PARTY_SIZE = [
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10)
        ]
        model = Booking
        fields = ('date', 'party_size', 'time_slot')
        # party_size widget has been changed so that users (except admin users
        # via the admin panel) are limited to making a booking for 1-10
        # guests only.
        widgets = {
            'party_size': Select(choices=PARTY_SIZE),
        }

    def __init__(self, user, *args, **kwargs):
        """
        __init__ method included so that the date widget can be
        made readonly to avoid users filling in the date field manually
        rather than using the datepicker and so that the identity of the
        user can be used in the clean methods.
        """
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'readonly': True})

    def get_timeslot_tables(self, time_slot):
        """
        Method to get all the tables allocated to a
        particular time slot.
        """
        time_slot_string = str(time_slot)
        time = TimeSlot.objects.get(time=time_slot_string)
        tables = time.tables.all()
        return tables

    def get_timeslot_capacity(self, tables):
        """
        Method to get the seating capacity of a
        particuar time slot.
        """
        time_slot_capacity = sum([table.size for table in tables])
        return time_slot_capacity

    def get_current_bookings(self, date, time_slot):
        """
        Method to get current bookings already made on the same date and for
        the same time slot.
        """
        current_bookings = Booking.objects.filter(date=date,
                                                  time_slot=time_slot)
        return current_bookings

    def get_capacity_booked(self, current_bookings):
        """
        Method to get the seating capacity of all the tables booked in
        the current_bookings.
        """
        all_booked_tables = []
        for booking in current_bookings:
            booked_tables = booking.tables.all()
            for booked_table in booked_tables:
                all_booked_tables.append(booked_table)
        capacity_booked = sum(
            [
                booked_table.size
                for booked_table in all_booked_tables
            ]
        )
        return capacity_booked

    def clean_date(self):
        """
        Method to clean the date field.

        This method makes sure that if the user tries to manipulate
        the booking id number in the url on the Edit Booking page to
        try and edit another user's booking, a ValidationError is raised.

        This method also prevents the user from making more than one booking
        per day by raising a ValidationError. In the case of the user editing
        a booking where the edited booking is for the same date as the original
        booking (so only the time_slot or party_size is changing), the original
        booking is excluded from the check.
        """
        user = self.user
        date = self.cleaned_data['date']

        # If the booking is a new booking, self.instance.id will be None
        # and all existing bookings for the user on the same date as the
        # new booking will be taken into account when checking if the user
        # already has a booking for that date.
        if self.instance.id is None:
            same_date_bookings = Booking.objects.filter(booker=user, date=date)
        # If the booking is an edited booking, self.instance.id will be the
        # booking id and the else statement will apply.
        else:
            # This checks whether the booker who made the original booking
            # is the same as the user who is trying to edit the booking.
            current_booking = get_object_or_404(Booking, id=self.instance.id)
            if current_booking.booker != user:
                raise ValidationError(
                    "You cannot change another guest's booking"
                )
            # The else statement applies if the booker who made the original
            # booking and the user who is trying to edit the booking are the
            # same.
            else:
                # If the user is editing a booking but only changing the
                # party_size or time_slot (so the date is not changing),
                # the existing booking needs to be excluded so that it
                # does not count when checking whether the user already
                # has a booking for that date.
                same_date = current_booking.date == date
                if same_date:
                    same_date_bookings = Booking.objects.filter(
                        booker=user, date=date
                    ).exclude(
                        id=self.instance.id
                    )
                # The else statement applies if the date of the original
                # booking and the date of the edited booking are different.
                else:
                    same_date_bookings = Booking.objects.filter(booker=user,
                                                                date=date)

        # If the number of bookings the user has on the same date as the
        # new or edited booking requested is more than 0, a ValidationError
        # is raised to prevent the user from having more than one booking per
        # day.
        if len(same_date_bookings) > 0:
            raise ValidationError('You can only have one booking per day')

        return date

    def clean_time_slot(self):
        """
        Method to clean the time_slot field.

        This method makes sure that the selected time slot has enough
        capacity to cater for the number of guests selected by the user for
        the booking and if the booking is for today, checks that the time_slot
        is not in the past.

        If the time slot cannot accommodate the user's booking on the
        selected date or the time slot is now in the past then a
        ValidationError is raised to inform the user.

        In the case of edited bookings, if a user is editing a booking but
        only changing the party_size i.e. the date and time_slot are not
        changing, the existing booking needs to be excluded from the
        current_bookings so that the table(s) allocated to the original
        booking will be included when the available seating capacity for
        the edited booking is calculated.
        """
        date = self.cleaned_data.get('date')
        time_slot = self.cleaned_data['time_slot']
        party_size = self.cleaned_data['party_size']

        # The if statement is required because the date could be
        # None if a ValidationError has been raised in the
        # clean_date method.
        if date and time_slot and party_size:
            tables = self.get_timeslot_tables(time_slot)
            time_slot_capacity = self.get_timeslot_capacity(tables)

            # If the new booking/edited booking is being made/edited for
            # today, this checks whether the time_slot the user is trying
            # to book for has passed.
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            time = getattr(time_slot, 'time')
            if date == current_date and time < current_time:
                raise ValidationError('You cannot book for a time in the past')

            # If the booking is a new booking, self.instance.id will be None
            # and all current bookings will be taken into account when
            # calculating the available seating capacity.
            if self.instance.id is None:
                current_bookings = self.get_current_bookings(date, time_slot)
            # If the booking is an edited booking, self.instance.id will be the
            # booking id. If the user is editing a booking but only changing
            # the party_size i.e. the date and time_slot are not changing,
            # the existing booking needs to be excluded from the
            # current_bookings so that the table(s) allocated to the original
            # booking will be included in the available seating capacity
            # calculated for the edited booking.
            else:
                current_booking = get_object_or_404(Booking,
                                                    id=self.instance.id)
                same_date = current_booking.date == date
                same_time_slot = current_booking.time_slot == time_slot

                if same_date and same_time_slot:
                    current_bookings = self.get_current_bookings(
                        date, time_slot
                    ).exclude(
                        id=self.instance.id
                    )
                else:
                    current_bookings = self.get_current_bookings(date,
                                                                 time_slot)

            if len(current_bookings) > 0:
                capacity_booked = self.get_capacity_booked(current_bookings)
            else:
                capacity_booked = 0

            if capacity_booked + party_size > time_slot_capacity:
                raise ValidationError('Sorry this booking is unavailable')

        return time_slot
