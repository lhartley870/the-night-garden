import datetime
from datetime import date, timedelta, time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Table, TimeSlot, Booking
from .forms import BookingForm


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

        self.user3 = User.objects.create_user(
            username='usertest3',
            password='789',
            email='usertest3@gmail.com',
            first_name='Lucy',
            last_name='Jones',
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
            name='freesia',
            size=2
        )

        self.table4 = Table.objects.create(
            name='orchid',
            size=2
        )

        self.table5 = Table.objects.create(
            name='tulip',
            size=6
        )

        self.table6 = Table.objects.create(
            name='primrose',
            size=2
        )

        self.table7 = Table.objects.create(
            name='dahlia',
            size=2
        )

        self.table8 = Table.objects.create(
            name='poppy',
            size=4
        )

        self.table9 = Table.objects.create(
            name='violet',
            size=8
        )

        self.time_now = datetime.datetime.now()
        self.two_hours_forward = self.time_now + timedelta(hours=2)
        self.two_half_hours_forward = self.time_now + timedelta(hours=2, minutes=30)
        self.three_hours_forward = self.time_now + timedelta(hours=3)

        self.time_slot1 = TimeSlot.objects.create(
            time=time(
                self.two_hours_forward.hour,
                self.two_hours_forward.minute
            )
        )
        self.time_slot1.tables.add(
            self.table1,
            self.table2,
            self.table3,
            self.table4,
            self.table5
        )

        self.time_slot2 = TimeSlot.objects.create(
            time=time(
                self.two_half_hours_forward.hour,
                self.two_half_hours_forward.minute
            )
        )

        self.time_slot2.tables.add(
            self.table6,
            self.table7,
            self.table8,
            self.table9
        )

        self.time_slot3 = TimeSlot.objects.create(
            time=time(
                self.three_hours_forward.hour,
                self.three_hours_forward.minute
            )
        )

        self.today = date.today()

        self.booking1 = Booking.objects.create(
            date=self.today + timedelta(days=14),
            booker=self.user1,
            party_size=4,
            time_slot=self.time_slot1,
        )
        self.booking1.tables.add(self.table2)

        self.booking2 = Booking.objects.create(
            date=self.today + timedelta(days=16),
            booker=self.user1,
            party_size=2,
            time_slot=self.time_slot1,
        )
        self.booking1.tables.add(self.table1)

        self.booking3 = Booking.objects.create(
            date=self.today + timedelta(days=17),
            booker=self.user3,
            party_size=2,
            time_slot=self.time_slot1,
        )
        self.booking3.tables.add(self.table1)
    
        self.booking4 = Booking.objects.create(
            date=self.today + timedelta(days=18),
            booker=self.user3,
            party_size=2,
            time_slot=self.time_slot1,
        )
        self.booking4.tables.add(self.table1)

        self.booking5 = Booking.objects.create(
            date=self.today + timedelta(days=19),
            booker=self.user3,
            party_size=2,
            time_slot=self.time_slot1,
        )
        self.booking5.tables.add(self.table1)

        self.booking6 = Booking.objects.create(
            date=self.today + timedelta(days=20),
            booker=self.user3,
            party_size=2,
            time_slot=self.time_slot1,
        )
        self.booking6.tables.add(self.table1)

        self.booking7 = Booking.objects.create(
            date=self.today + timedelta(days=21),
            booker=self.user3,
            party_size=2,
            time_slot=self.time_slot1,
        )
        self.booking7.tables.add(self.table1)

        self.booking8 = Booking.objects.create(
            date=self.today + timedelta(days=22),
            booker=self.user3,
            party_size=2,
            time_slot=self.time_slot1,
        )
        self.booking8.tables.add(self.table1)

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

    # Check context rendered for my_bookings page context is correct
    # where the user has no bookings.
    def test_my_bookings_page_context_no_bookings(self):
        self.client.login(username='usertest2', password='456')
        response = self.client.get(reverse('my_bookings'))
        bookings = Booking.objects.filter(booker=self.user2)
        duplicate_booking_dates = []
        self.assertQuerysetEqual(
            response.context['bookings'],
            bookings,
            transform=lambda x: x
        )
        self.assertEqual(len(response.context['page_obj']), 0)
        self.assertEqual(
            response.context['duplicate_booking_dates'],
            duplicate_booking_dates
        )

    # Check context rendered for my_bookings page context is correct
    # where the user has 6 future bookings with no duplicate booking
    # dates.
    def test_my_bookings_context_6_future_bookings_no_duplicate_dates(self):
        self.client.login(username='usertest3', password='789')
        response = self.client.get(reverse('my_bookings'))
        bookings = Booking.objects.filter(booker=self.user3)
        duplicate_booking_dates = []
        self.assertQuerysetEqual(
            response.context['bookings'],
            bookings,
            transform=lambda x: x
        )
        self.assertEqual(len(response.context['page_obj']), 6)
        self.assertEqual(
            response.context['duplicate_booking_dates'],
            duplicate_booking_dates
        )

    # Check context rendered for my_bookings page context is correct
    # where the user has 6 future bookings and one past booking on a previous
    # date with no duplicate booking dates.
    def test_my_bookings_context_1_past_booking_no_duplicate_dates(self):
        # Create a new past booking for user3 for yesterday.
        booking9 = Booking.objects.create(
            date=self.today - timedelta(days=1),
            booker=self.user3,
            party_size=2,
            time_slot=self.time_slot1,
        )
        booking9.tables.add(self.table1)

        self.client.login(username='usertest3', password='789')
        response = self.client.get(reverse('my_bookings'))
        # booking9 for yesterday should be excluded from the bookings
        # variable.
        bookings = Booking.objects.filter(
            booker=self.user3
        ).exclude(
            id=booking9.id
        )
        duplicate_booking_dates = []
        self.assertQuerysetEqual(
            response.context['bookings'],
            bookings,
            transform=lambda x: x
        )
        self.assertEqual(len(response.context['page_obj']), 6)
        self.assertEqual(
            response.context['duplicate_booking_dates'],
            duplicate_booking_dates
        )

    # Check context rendered for my_bookings page context is correct
    # where the user has 6 future bookings and one past booking today
    # with no duplicate booking dates.
    def test_my_bookings_context_1_past_booking_today_no_duplicate_dates(self):
        # Create a new booking for user3 for today for a time that has passed.
        one_hour_ago = self.time_now - timedelta(hours=1)
        time_slot2 = TimeSlot.objects.create(
            time=time(one_hour_ago.hour, one_hour_ago.minute)
        )
        time_slot2.tables.add(self.table5)

        booking9 = Booking.objects.create(
            date=self.today,
            booker=self.user3,
            party_size=6,
            time_slot=time_slot2,
        )
        booking9.tables.add(self.table5)

        self.client.login(username='usertest3', password='789')
        response = self.client.get(reverse('my_bookings'))
        # booking9 for today for a time that has passed should be excluded
        # from the bookings variable.
        current_date = self.today
        current_time = self.time_now
        bookings = Booking.objects.filter(
            booker=self.user3
        ).exclude(
            date__lt=current_date
        ).exclude(
            date=current_date,
            time_slot__time__lt=current_time
        )
        duplicate_booking_dates = []
        self.assertQuerysetEqual(
            response.context['bookings'],
            bookings,
            transform=lambda x: x
        )
        self.assertEqual(len(response.context['page_obj']), 6)
        self.assertEqual(
            response.context['duplicate_booking_dates'],
            duplicate_booking_dates
        )

    # Check context rendered for my_bookings page context is correct
    # where the user has 6 future bookings made by the user and 2 future
    # bookings made by admin for the user for a large party of 20 over 
    # 2 timeslots so there are duplicate booking dates.
    def test_my_bookings_context_duplicate_dates(self):
        # Create a new booking for user3 for today for 16 guests for time_slot1.
        booking9 = Booking.objects.create(
            date=self.today + timedelta(days=23),
            booker=self.user3,
            party_size=16,
            time_slot=self.time_slot1,
        )
        booking9.tables.add(
            self.table1,
            self.table2,
            self.table3,
            self.table4,
            self.table5
        )
        # Create a new booking for user3 for today for 4 guests for time_slot2.
        booking10 = Booking.objects.create(
            date=self.today + timedelta(days=23),
            booker=self.user3,
            party_size=4,
            time_slot=self.time_slot2,
        )
        booking10.tables.add(self.table8)

        self.client.login(username='usertest3', password='789')
        response = self.client.get(reverse('my_bookings'))
        bookings = Booking.objects.filter(booker=self.user3)

        # Today's date should appear twice in duplicate_booking_dates
        # - once for booking9 and once for booking10.
        duplicate_booking_dates = [booking9.date, booking10.date]
        self.assertQuerysetEqual(
            response.context['bookings'],
            bookings,
            transform=lambda x: x
        )
        self.assertEqual(len(response.context['page_obj']), 6)
        self.assertEqual(
            response.context['duplicate_booking_dates'],
            duplicate_booking_dates
        )

    # Get make booking page and check correct templates are rendered.
    def test_get_make_booking_page(self):
        self.client.login(username='usertest', password='123')
        response = self.client.get(reverse('make_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'make_booking.html')

    # Check context rendered for make_booking page is correct.
    def test_my_bookings_context(self):
        self.client.login(username='usertest', password='123')
        response = self.client.get(reverse('make_booking'))
        initial_date = self.today
        closed_day = self.today.weekday() == 0 or self.today.weekday() == 1
        christmas_closed_dates = [
            date(2022, 12, 24),
            date(2022, 12, 25),
            date(2022, 12, 28),
            date(2022, 12, 29),
            date(2022, 12, 30),
            date(2022, 12, 31),
            date(2023, 1, 1)
        ]
        if closed_day:
            if self.today.weekday() == 0:
                initial_date = self.today + timedelta(days=2)
            else:
                initial_date = self.today + timedelta(days=1)

        if self.today in christmas_closed_dates:
            initial_date = date(2023, 1, 4)

        initial_data = {
            'date': initial_date
        }
        booking_form = BookingForm(user=None, initial=initial_data)
        self.assertEqual(
                response.context['booking_form'].__dict__['initial']['date'],
                booking_form.__dict__['initial']['date'],
        )

    # Check that user can make a valid booking and is redirected to the 
    # my_bookings page.
    def test_can_make_valid_booking(self):
        self.client.login(username='usertest', password='123')
        response = self.client.post(
                    reverse('make_booking'),
                    data={
                        'date': self.today + timedelta(days=18),
                        'party_size': 2,
                        'time_slot': self.time_slot1.id
                        })
        self.assertRedirects(response, reverse('my_bookings'))

    # Check that user making an invalid booking remains on the 
    # make_booking page.
    def test_make_invalid_booking(self):
        self.client.login(username='usertest', password='123')
        response = self.client.post(
                    reverse('make_booking'),
                    data={
                        'date': self.today + timedelta(days=14),
                        'party_size': 2,
                        'time_slot': self.time_slot1.id
                        })
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

    # Check that user can validly edit a booking and is redirected to
    # the my_bookings page.
    def test_can_edit_booking(self):
        self.client.login(username='usertest', password='123')
        response = self.client.post(
                    reverse('edit_booking', args=[self.booking1.id]),
                    data={
                        'date': self.today + timedelta(days=20),
                        'party_size': 2,
                        'time_slot': self.time_slot1.id
                        })
        self.assertRedirects(response, reverse('my_bookings'))

    # Check that user invalidly editing a booking remains on the 
    # edit_booking page.
    def test_edit_invalid_booking(self):
        self.client.login(username='usertest', password='123')
        response = self.client.post(
                    reverse('edit_booking', args=[self.booking1.id]),
                    data={
                        'date': self.today + timedelta(days=16),
                        'party_size': 2,
                        'time_slot': self.time_slot1.id
                        })
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

    # Test TableSelectionMixin - only 1 table available to book. 
    def test_one_table_available(self):
        self.time_slot3.tables.add(self.table5)
        self.client.login(username='usertest', password='123')
        response = self.client.post(
                    reverse('make_booking'),
                    data={
                        'date': self.today + timedelta(days=20),
                        'party_size': 2,
                        'time_slot': self.time_slot3.id
                        })
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_table = created_booking.tables.all()
        table5 = Table.objects.filter(id=self.table5.id)
        self.assertQuerysetEqual(
            booking_table,
            table5,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - only 1 exact match table available to book. 
    def test_one_match_table_available(self):
        self.time_slot3.tables.add(self.table1, self.table5)
        self.client.login(username='usertest', password='123')
        response = self.client.post(
                    reverse('make_booking'),
                    data={
                        'date': self.today + timedelta(days=20),
                        'party_size': 2,
                        'time_slot': self.time_slot3.id
                        })
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_table = created_booking.tables.all()
        table1 = Table.objects.filter(id=self.table1.id)
        self.assertQuerysetEqual(
            booking_table,
            table1,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - 2 exact match tables available to book. 
    def test_two_match_tables_available(self):
        self.time_slot3.tables.add(self.table1, self.table3)
        self.client.login(username='usertest', password='123')
        response = self.client.post(
                    reverse('make_booking'),
                    data={
                        'date': self.today + timedelta(days=20),
                        'party_size': 2,
                        'time_slot': self.time_slot3.id
                        })
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        tables = created_booking.tables.all()
        tables_1_and_3 = [
            str(Table.objects.filter(id=self.table1.id)),
            str(Table.objects.filter(id=self.table3.id))
        ]
        self.assertIn(
            str(tables),
            tables_1_and_3,
        )
