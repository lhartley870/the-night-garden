import datetime
from django.urls import reverse
from django.test import TestCase
from django.contrib import admin
from django.contrib.auth.models import User
from .admin import TimeSlotAdmin, BookingAdmin
from .models import Table, TimeSlot, Booking


class TestAdmin(TestCase):

    # Set up test user, tables, timeslots and booking.
    def setUp(self):

        self.user = User.objects.create_user(
            username='usertest',
            password='123',
            email='usertest@gmail.com',
            first_name='Joe',
            last_name='Bloggs',
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

        self.time_slot1 = TimeSlot.objects.create(
            time=datetime.time(18, 30)
        )
        self.time_slot1.tables.add(self.table1, self.table2)

        self.time_slot2 = TimeSlot.objects.create(
            time=datetime.time(19, 00)
        )
        self.time_slot2.tables.add(self.table3, self.table4)

        self.booking1 = Booking.objects.create(
            date=datetime.date(2022, 6, 6),
            booker=self.user,
            party_size=4,
            time_slot=self.time_slot1,
        )
        self.booking1.tables.add(self.table2)

        self.username = 'admin5'
        self.password = 'staff**'

    # Test the allocated_tables mixin method for the TimeSlotAdmin
    # ModelAdmin object.
    def test_timeslot_allocated_tables(self):
        # Code for testing django admin custom functions adapted from
        # answers given by giantas and Alex V on this Stack Overflow
        # post - https://stackoverflow.com/questions/40724534/coverage
        # -test-django-admin-custom-functions
        time_slot = self.time_slot1
        time_slot_admin = TimeSlotAdmin(TimeSlot, admin.site)
        obj = time_slot_admin.get_object(None, time_slot.id)
        admin_allocated_tables = time_slot_admin.allocated_tables(obj)
        self.assertEqual(admin_allocated_tables, 'rose (2), lily (4)')

    # Test the booking_time method for the TimeSlotAdmin ModelAdmin object.
    def test_timeslot_booking_time(self):
        time_slot = self.time_slot2
        time_slot_admin = TimeSlotAdmin(TimeSlot, admin.site)
        obj = time_slot_admin.get_object(None, time_slot.id)
        admin_booking_time = time_slot_admin.booking_time(obj)
        self.assertEqual(admin_booking_time, '19:00')

    # Test the allocated_tables mixin method for the BookingAdmin
    # ModelAdmin object.
    def test_booking_allocated_tables(self):
        booking = self.booking1
        booking_admin = BookingAdmin(Booking, admin.site)
        obj = booking_admin.get_object(None, booking.id)
        admin_allocated_tables = booking_admin.allocated_tables(obj)
        self.assertEqual(admin_allocated_tables, 'lily (4)')

    # Test the booking_date method for the BookingAdmin ModelAdmin object.
    def test_booking_booking_date(self):
        booking = self.booking1
        booking_admin = BookingAdmin(Booking, admin.site)
        obj = booking_admin.get_object(None, booking.id)
        admin_booking_date = booking_admin.booking_date(obj)
        self.assertEqual(admin_booking_date, '2022-06-06')

    # Test the admin approval of booking1 created in setUp above.
    def test_approve_bookings(self):
        # Code for testing admin actions in django adapted from
        # answers given by catavaran, Wtower and radtek on this
        # Stack Overflow post - https://stackoverflow.com/questions
        # /29026779/testing-custom-admin-actions-in-django

        self.user = User.objects.create_superuser(
            self.username,
            'admin@example.com',
            self.password
        )

        # Check the number of bookings which are already approved.
        approved_bookings = Booking.objects.filter(approved=True).count()
        self.assertFalse(self.booking1.approved)

        data = {'action': 'approve_bookings',
                '_selected_action': [self.booking1.id, ]}
        change_url = reverse('admin:booking_booking_changelist')
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(change_url, data, follow=True)
        self.client.logout()

        self.assertEqual(response.status_code, 200)

        # Check that the number of approved bookings has gone up by 1.
        self.assertEqual(
            Booking.objects.filter(approved=True).count(),
            approved_bookings+1
        )
