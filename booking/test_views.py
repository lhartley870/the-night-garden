import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Table, TimeSlot, Booking


# Create your tests here.
class TestForms(TestCase):

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

        self.time_slot1 = TimeSlot.objects.create(
            time=datetime.time(18, 30, 00)
        )
        self.time_slot1.tables.add(self.table1, self.table2)

        self.booking1 = Booking.objects.create(
            date=datetime.date(2022, 3, 12),
            booker=self.user,
            party_size=4,
            time_slot=self.time_slot1,
        )
        self.booking1.tables.add(self.table2)

    # Get home page and check correct templates are rendered.
    def test_get_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'index.html')

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
    
    # Check that a booking can be deleted.
    def test_can_delete_booking(self):
        self.client.login(username='usertest', password='123')

        booking2 = Booking.objects.create(
            date=datetime.date(2022, 4, 25),
            booker=self.user,
            party_size=4,
            time_slot=self.time_slot1,
        )
        booking2.tables.add(self.table2)

        response = self.client.post(reverse(
                                    'cancel_booking',
                                    args=[booking2.id]))
        self.assertRedirects(response, reverse('my_bookings'))
        booking2_matches = Booking.objects.filter(id=booking2.id)
        self.assertEqual(len(booking2_matches), 0)