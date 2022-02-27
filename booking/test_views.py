import datetime
from datetime import date, timedelta, time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Table, TimeSlot, Booking


# Create your tests here.
class TestViews(TestCase):

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

        self.time_now = datetime.datetime.now()
        self.two_hours_forward = self.time_now + timedelta(hours=2)

        self.time_slot1 = TimeSlot.objects.create(
            time=time(
                self.two_hours_forward.hour,
                self.two_hours_forward.minute
            )
        )
        self.time_slot1.tables.add(self.table1, self.table2)

        self.today = date.today()

        self.booking1 = Booking.objects.create(
            date=self.today + timedelta(days=14),
            booker=self.user,
            party_size=4,
            time_slot=self.time_slot1,
        )
        self.booking1.tables.add(self.table2)

        self.booking2 = Booking.objects.create(
            date=self.today + timedelta(days=16),
            booker=self.user,
            party_size=2,
            time_slot=self.time_slot1,
        )
        self.booking1.tables.add(self.table1)

    # Get home page and check correct templates are rendered.
    def test_get_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'index.html')

    # Get register/signup page and check correct templates are rendered.
    def test_get_register_page(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'account/signup.html')

    # Get login page and check correct templates are rendered.
    def test_login_page(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'account/login.html')

    # Get my bookings page and check correct templates are rendered.
    def test_get_my_bookings_page(self):
        self.client.login(username='usertest', password='123')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'my_bookings.html')

    # Get make booking page and check correct templates are rendered.
    def test_get_make_booking_page(self):
        self.client.login(username='usertest', password='123')
        response = self.client.get(reverse('make_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'make_booking.html')

    # Get edit booking page and check correct templates are rendered.
    def test_get_edit_booking_page(self):
        self.client.login(username='usertest', password='123')
        response = self.client.get(reverse('edit_booking', args=[self.booking1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'edit_booking.html')

    # Get menus page and check correct templates are rendered.
    def test_get_menus_page(self):
        response = self.client.get(reverse('menus'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'menus.html')

    # Get contact us page and check correct templates are rendered.
    def test_get_contact_us_page(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'contact.html')

    # Get logout page and check correct templates are rendered.
    def test_logout_page(self):
        self.client.login(username='usertest', password='123')
        response = self.client.get(reverse('account_logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'account/logout.html')

    # Check that a booking can be deleted.
    def test_can_delete_booking(self):
        self.client.login(username='usertest', password='123')

        booking = Booking.objects.create(
            date=self.today + timedelta(days=22),
            booker=self.user1,
            party_size=4,
            time_slot=self.time_slot1,
        )
        booking.tables.add(self.table2)

        response = self.client.post(reverse(
                                    'cancel_booking',
                                    args=[booking.id]))
        self.assertRedirects(response, reverse('my_bookings'))
        booking_matches = Booking.objects.filter(id=booking.id)
        self.assertEqual(len(booking_matches), 0)