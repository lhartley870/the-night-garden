import datetime
from unittest import mock
import pytz
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Table, TimeSlot, Booking


# Create your tests here.
class TestModels(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='usertest',
            password='123',
            email='usertest@gmail.com',
            first_name='Joe',
            last_name='Bloggs',
        )

        self.table1 = Table.objects.create(
            name='Rose',
            size=2
        )

        self.table2 = Table.objects.create(
            name='LILY',
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

        self.time_slot1 = TimeSlot.objects.create(
            time=datetime.time(18, 30, 2)
        )
        self.time_slot1.tables.add(self.table1, self.table2)

        self.time_slot2 = TimeSlot.objects.create(
            time=datetime.time(19, 00, 00)
        )
        self.time_slot2.tables.add(self.table3, self.table4)

        self.booking = Booking.objects.create(
            date=datetime.date(2022, 3, 12),
            booker=self.user,
            party_size=4,
            time_slot=self.time_slot1,
        )
        self.booking.tables.add(self.table2,)

    # Test the string method for the Table model.
    def test_table_string_method_returns_table_name(self):
        table = Table.objects.get(pk=self.table1.pk)
        self.assertEqual(str(table.name), 'rose')

    # Test the NameField field subclass for the Table model.
    def test_namefield_creates_lowercase_table_name(self):
        table = Table.objects.get(pk=self.table2.pk)
        self.assertEqual(table.name, 'lily')

    # Test the string method for the TimeSlot model.
    def test_timeslot_string_method_returns_time_in_hrs_and_mins(self):
        self.assertEqual(str(self.time_slot1), '18:30')

    # Test the string method for the Booking model.
    def test_booking_string_method_returns_expected_sentence(self):
        self.assertEqual(str(self.booking),
                         'Booking #1 on 12 March 2022 for 4 guest(s) at 18:30')

    # Test the date_string method for the Booking model.
    def test_booking_date_string_method_returns_formatted_date(self):
        self.assertEqual(self.booking.date_string(), '12 March 2022')

    # Test the created_on default method for the Booking model.
    def test_created_on_timestamp(self):
        # Code for testing the created_on method adapted from an answer
        # given by neverwalkaloner and edited by vidstige on this
        # Stack Overflow post - https://stackoverflow.com/questions/
        # 49874923/how-to-test-auto-now-add-in-django
        mocked = datetime.datetime(2022, 3, 2, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now',
                        mock.Mock(return_value=mocked)):
            booking2 = Booking.objects.create(
                date=datetime.date(2022, 3, 15),
                booker=self.user,
                party_size=5,
                time_slot=self.time_slot2,
            )
            self.booking.tables.add(self.table3,)
            self.assertEqual(booking2.created_on, mocked)

    # Test that the Booking model approved field has the expected
    # default value.
    def test_approved_defaults_to_false(self):
        self.assertFalse(self.booking.approved)
