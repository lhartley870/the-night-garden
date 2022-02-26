import datetime
from datetime import date, timedelta, time
from django.test import TestCase
from django.contrib.auth.models import User
from .forms import TimeSlotForm, CustomSignUpForm, BookingForm
from .models import Table, TimeSlot, Booking


# Create your tests here.
class TestForms(TestCase):

    # Set up test users, tables, times, time_slots and bookings.
    def setUp(self):

        self.user1 = User.objects.create_user(
            username='usertest',
            password='123',
            email='usertest@gmail.com',
            first_name='Joe',
            last_name='Bloggs',
        )

        self.user2 = User.objects.create_user(
            username='usertest2',
            password='456',
            email='usertest2@gmail.com',
            first_name='John',
            last_name='Smith',
        )

        self.table1 = Table.objects.create(
            name='rose',
            size=2
        )

        self.table2 = Table.objects.create(
            name='lily',
            size=4
        )

        self.table3 = Table.objects.create(
            name='tulip',
            size=6
        )

        self.table4 = Table.objects.create(
            name='violet',
            size=8
        )

        self.table5 = Table.objects.create(
            name='dahlia',
            size=2
        )

        self.table6 = Table.objects.create(
            name='poppy',
            size=4
        )

        self.table7 = Table.objects.create(
            name='primrose',
            size=8
        )

        self.table8 = Table.objects.create(
            name='daffodil',
            size=2
        )

        self.time_1 = time(18, 30)
        self.time_2 = time(16, 15)
        self.time_3 = time(17, 15)
        self.time_4 = time(23, 00)

        self.time_now = datetime.datetime.now()
        self.one_hour_ago = self.time_now - timedelta(hours=1)
        self.one_hour_forward = self.time_now + timedelta(hours=1)
        self.two_hours_forward = self.time_now + timedelta(hours=2)
        self.four_hours_forward = self.time_now + timedelta(hours=4)

        self.time_slot1 = TimeSlot.objects.create(
            time=time(
                self.two_hours_forward.hour,
                self.two_hours_forward.minute
            )
        )
        self.time_slot1.tables.add(self.table1, self.table2)

        self.time_slot2 = TimeSlot.objects.create(
            time=time(
                self.four_hours_forward.hour,
                self.four_hours_forward.minute
            )
        )
        self.time_slot2.tables.add(self.table3, self.table4)

        self.time_slot3 = TimeSlot.objects.create(
            time=time(self.one_hour_ago.hour, self.one_hour_ago.minute)
        )
        self.time_slot3.tables.add(self.table5, self.table6)

        self.time_slot4 = TimeSlot.objects.create(
            time=time(self.one_hour_forward.hour, self.one_hour_forward.minute)
        )
        self.time_slot4.tables.add(self.table7, self.table8)

        self.today = date.today()

        self.booking1 = Booking.objects.create(
            date=self.today + timedelta(days=14),
            booker=self.user1,
            party_size=4,
            time_slot=self.time_slot1,
        )
        self.booking1.tables.add(self.table2,)

        self.booking2 = Booking.objects.create(
            date=self.today + timedelta(days=17),
            booker=self.user1,
            party_size=6,
            time_slot=self.time_slot2,
        )
        self.booking2.tables.add(self.table3,)

        self.booking3 = Booking.objects.create(
            date=self.today + timedelta(days=22),
            booker=self.user2,
            party_size=2,
            time_slot=self.time_slot1,
        )
        self.booking3.tables.add(self.table1)

    # Test that the TimeSlotForm time field is required.
    def test_timeslotform_time_field_is_required(self):
        form = TimeSlotForm({'time': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors.keys())
        self.assertEqual(form.errors['time'][0], 'This field is required.')

    # Test that the TimeSlotForm tables field is required.
    def test_timeslotform_tables_field_is_required(self):
        form = TimeSlotForm({'tables': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('tables', form.errors.keys())
        self.assertEqual(form.errors['tables'][0], 'This field is required.')

    # Test that the time and tables fields are named as explicit
    # fields in the TimeSlotForm.
    def test_fields_are_explicit_in_timeslotform_metaclass(self):
        form = TimeSlotForm()
        self.assertEqual(form.Meta.fields, ('time', 'tables'))

    # Test the TimeSlotForm clean_time method for a valid time.
    def test_timeslot_form_clean_time_method_valid_time(self):
        data = {
            "time": self.time_1,
            "tables": (self.table1, self.table2)
        }

        form = TimeSlotForm(data)
        self.assertTrue(form.is_valid())

    # Test the TimeSlotForm clean_time method for an invalid early time.
    def test_timeslot_form_clean_time_method_invalid_early_time(self):
        data = {
            "time": self.time_2,
            "tables": (self.table1, self.table2)
        }

        form = TimeSlotForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['time'], ["Time slots must be between 17:30 and 22:00"]
        )

    # Test the TimeSlotForm clean_time method for an invalid early time
    # after 5pm.
    def test_timeslot_form_clean_time_method_invalid_early_time_after_5(self):
        data = {
            "time": self.time_3,
            "tables": (self.table1, self.table2)
        }

        form = TimeSlotForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['time'], ["Time slots must be between 17:30 and 22:00"]
        )

    # Test the TimeSlotForm clean_time method for an invalid late time.
    def test_timeslot_form_clean_time_method_invalid_late_time(self):
        data = {
            "time": self.time_4,
            "tables": (self.table1, self.table2)
        }

        form = TimeSlotForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['time'], ["Time slots must be between 17:30 and 22:00"]
        )

    # Test that the CustomSignUpForm first name field is required.
    def test_customsignupform_first_name_field_is_required(self):
        form = CustomSignUpForm({'first_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.keys())
        self.assertEqual(
            form.errors['first_name'][0],
            'This field is required.'
        )

    # Test that the CustomSignUpForm last name field is required.
    def test_customsignupform_last_name_field_is_required(self):
        form = CustomSignUpForm({'last_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors.keys())
        self.assertEqual(
            form.errors['last_name'][0],
            'This field is required.'
        )

    # Test that the CustomSignUpForm first name field must be letters only.
    def test_customsignupform_first_name_field_is_letters(self):
        form = CustomSignUpForm({'first_name': '11112222abc'})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.keys())
        self.assertEqual(
            form.errors['first_name'][0],
            'Only letters are allowed.'
        )

    # Test that the CustomSignUpForm last name field must be letters only.
    def test_customsignupform_last_name_field_is_letters(self):
        form = CustomSignUpForm({'last_name': '11112222abc'})
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors.keys())
        self.assertEqual(
            form.errors['last_name'][0],
            'Only letters are allowed.'
        )

    # Test that the CustomSignUpForm first name widget is a TextField.
    def test_customsignupform_first_name_widget_is_textfield(self):
        form = CustomSignUpForm()
        self.assertEqual(
            form.fields['first_name'].widget.__class__.__name__,
            'TextInput'
        )

    # Test that the CustomSignUpForm last name widget is a TextField.
    def test_customsignupform_last_name_widget_is_textfield(self):
        form = CustomSignUpForm()
        self.assertEqual(
            form.fields['last_name'].widget.__class__.__name__,
            'TextInput'
        )

    # Test that BookingForm date field is required.
    def test_bookingform_date_field_is_required(self):
        form = BookingForm(user=self.user1, data={'date': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors.keys())
        self.assertEqual(form.errors['date'][0], 'This field is required.')

    # Test that BookingForm party size field is required.
    def test_bookingform_party_size_field_is_required(self):
        form = BookingForm(user=self.user1, data={'party_size': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('party_size', form.errors.keys())
        self.assertEqual(
            form.errors['party_size'][0],
            'This field is required.'
        )

    # Test that BookingForm time slot field is required.
    def test_bookingform_time_slot_field_is_required(self):
        form = BookingForm(user=self.user1, data={'time_slot': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('time_slot', form.errors.keys())
        self.assertEqual(
            form.errors['time_slot'][0],
            'This field is required.'
        )

    # Test that the date, party size and time slot fields are named as explicit
    # fields in the BookingForm.
    def test_fields_are_explicit_in_bookingform_metaclass(self):
        form = BookingForm(user=self.user1)
        self.assertEqual(form.Meta.fields, ('date', 'party_size', 'time_slot'))

    # Test that the BookingForm party size widget is a Select.
    def test_bookingform_party_size_widget_is_select(self):
        form = BookingForm(user=self.user1)
        self.assertEqual(
            form.fields['party_size'].widget.__class__.__name__,
            'Select'
        )

    # Test that the BookingForm date widget is readonly.
    def test_bookingform_date_widget_is_readonly(self):
        form = BookingForm(user=self.user1)
        self.assertTrue(form.fields['date'].widget.attrs['readonly'])

    # Test the BookingForm clean_date method for a valid date and new booking.
    def test_booking_form_clean_date_method_valid_date_new_booking(self):
        data = {
            "date": self.today + timedelta(days=27),
            "party_size": 4,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data)
        self.assertTrue(form.is_valid())

    # Test the BookingForm clean_date method for an invalid date
    # and new booking.
    def test_booking_form_clean_date_method_invalid_date_new_booking(self):
        data = {
            "date": self.today + timedelta(days=14),
            "party_size": 4,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['date'], ["You can only have one booking per day"]
        )

    # Test the BookingForm clean_date method for editing a booking
    # to another valid date.
    def test_booking_form_clean_date_method_valid_date_edited_booking(self):
        data = {
            "date": self.today + timedelta(days=15),
            "party_size": 4,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data, instance=self.booking1)
        self.assertTrue(form.is_valid())

    # Test the BookingForm clean_date method for editing a
    # booking to another invalid date.
    def test_booking_form_clean_date_method_invalid_date_edited_booking(self):
        data = {
            "date": self.today + timedelta(days=17),
            "party_size": 4,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data, instance=self.booking1)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['date'], ["You can only have one booking per day"]
        )

    # Test the BookingForm clean_date method for editing a booking for
    # the same date but with a different party_size.
    def test_booking_form_clean_date_method_same_date_edited_booking(self):
        data = {
            "date": self.today + timedelta(days=14),
            "party_size": 3,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data, instance=self.booking1)
        self.assertTrue(form.is_valid())

    # Test the BookingForm clean_date method for editing another
    # user's booking.
    def test_booking_form_clean_date_method_edit_another_user_booking(self):
        data = {
            "date": self.today + timedelta(days=19),
            "party_size": 3,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data, instance=self.booking3)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['date'], ["You cannot change another guest's booking"]
        )

    # Test the BookingForm clean_time_slot method for a new booking today
    # for a time in the past.
    def test_booking_form_clean_time_new_booking_today_time_in_past(self):
        data = {
            "date": self.today,
            "party_size": 2,
            "time_slot": self.time_slot3,
        }
        form = BookingForm(user=self.user1, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['time_slot'],
            ["You cannot book for a time in the past"]
        )

    # Test the BookingForm clean_time_slot method for a new booking today
    # for a time in the future.
    def test_booking_form_clean_time_new_booking_today_time_in_future(self):
        data = {
            "date": self.today,
            "party_size": 2,
            "time_slot": self.time_slot4,
        }
        form = BookingForm(user=self.user1, data=data)
        self.assertTrue(form.is_valid())

    # Test the BookingForm clean_time_slot method for an edited booking
    # today for a time in the past.
    def test_booking_form_clean_time_edited_booking_today_time_in_past(self):
        data = {
            "date": self.today,
            "party_size": 2,
            "time_slot": self.time_slot3,
        }
        form = BookingForm(user=self.user1, data=data, instance=self.booking1)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['time_slot'],
            ["You cannot book for a time in the past"]
        )

    # Test the BookingForm clean_time_slot method for an edited booking
    # today for a time in the future.
    def test_booking_form_clean_time_edited_booking_today_time_in_future(self):
        data = {
            "date": self.today,
            "party_size": 2,
            "time_slot": self.time_slot4,
        }
        form = BookingForm(user=self.user1, data=data, instance=self.booking1)
        self.assertTrue(form.is_valid())

    # Test the BookingForm clean_time_slot method for a new booking
    # not today where there is enough seating capacity for the booking
    # in the chosen time_slot.
    def test_booking_form_clean_time_valid_new_booking(self):
        data = {
            "date": self.today + timedelta(days=22),
            "party_size": 4,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data)
        self.assertTrue(form.is_valid())

    # Test the BookingForm clean_time_slot method for an edited booking
    # on a different date where there is enough seating capacity for the
    # amended booking.
    def test_booking_form_clean_time_valid_edited_booking(self):
        data = {
            "date": self.today + timedelta(days=22),
            "party_size": 4,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data, instance=self.booking1)
        self.assertTrue(form.is_valid())

    # Test the BookingForm clean_time_slot method for an edited booking for
    # the same date and time_slot as the original booking but for a different
    # party_size where there is enough seating capacity for the amended booking
    # taking into account the seating capacity that was allocated to the
    # original booking.
    def test_booking_form_clean_time_valid_same_day_edited_booking(self):
        data = {
            "date": self.today + timedelta(days=14),
            "party_size": 6,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data, instance=self.booking1)
        self.assertTrue(form.is_valid())

    # Test the BookingForm clean_time_slot method for a new booking not today
    # where there is not enough seating capacity for the booking in the
    # chosen time_slot.
    def test_booking_form_clean_time_invalid_new_booking(self):
        data = {
            "date": self.today + timedelta(days=22),
            "party_size": 6,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['time_slot'], ["Sorry this booking is unavailable"]
        )

    # Test the BookingForm clean_time_slot method for an edited booking
    # not today where there is not enough seating capacity for the booking
    # in the chosen time_slot.
    def test_booking_form_clean_time_invalid_edited_booking(self):
        data = {
            "date": self.today + timedelta(days=22),
            "party_size": 6,
            "time_slot": self.time_slot1,
        }
        form = BookingForm(user=self.user1, data=data, instance=self.booking1)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['time_slot'], ["Sorry this booking is unavailable"]
        )

    # Test BookingForm get_timeslot_tables method.
    def test_booking_form_get_timeslot_tables_method(self):
        form = BookingForm(user=None)
        time_slot = self.time_slot1
        time_slot_tables = Table.objects.filter(table_timeslots=time_slot)
        # Code for testing whether querysets are equal in django taken from
        # an answer given by dspacejs on this Stack Overflow post -
        # https://stackoverflow.com/questions/17685023/how-do-i-test-
        # django-querysets-are-equal
        self.assertQuerysetEqual(
            form.get_timeslot_tables(time_slot),
            time_slot_tables, transform=lambda x: x
        )

    # Test BookingForm get_timeslot_capacity method.
    def test_booking_form_get_timeslot_capacity_method(self):
        form = BookingForm(user=None)
        time_slot = self.time_slot1
        time_slot_tables = Table.objects.filter(table_timeslots=time_slot)
        self.assertEqual(form.get_timeslot_capacity(time_slot_tables), 6)

    # Test BookingForm get_current_bookings method.
    def test_booking_form_get_current_bookings_method(self):
        form = BookingForm(user=None)
        test_date = self.today + timedelta(days=14)
        time_slot = self.time_slot1
        booking = Booking.objects.filter(id=self.booking1.id)
        self.assertQuerysetEqual(
            form.get_current_bookings(test_date, time_slot),
            booking, transform=lambda x: x
        )

    # Test BookingForm get_capacity_booked method.
    def test_booking_form_get_capacity_booked_method(self):
        form = BookingForm(user=None)
        current_bookings = Booking.objects.filter(id=self.booking1.id)
        self.assertEqual(form.get_capacity_booked(current_bookings), 4)
