import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .forms import TimeSlotForm, CustomSignUpForm, BookingForm
from .models import Table, TimeSlot, Booking


# Create your tests here.
class TestForms(TestCase):

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

        self.time_1 = datetime.time(18, 30, 2)
        self.time_2 = datetime.time(16, 15, 00)
        self.time_3 = datetime.time(17, 15, 00)
        self.time_4 = datetime.time(23, 00, 00)

        self.time_slot1 = TimeSlot.objects.create(
            time=datetime.time(17, 30, 2)
        )
        self.time_slot1.tables.add(self.table1, self.table2)

        self.time_slot2 = TimeSlot.objects.create(
            time=datetime.time(20, 30, 00)
        )
        self.time_slot2.tables.add(self.table3, self.table4)

        self.booking1 = Booking.objects.create(
            date=datetime.date(2022, 3, 12),
            booker=self.user1,
            party_size=4,
            time_slot=self.time_slot1,
        )
        self.booking1.tables.add(self.table2,)

        self.booking2 = Booking.objects.create(
            date=datetime.date(2022, 3, 15),
            booker=self.user1,
            party_size=6,
            time_slot=self.time_slot2,
        )
        self.booking2.tables.add(self.table3,)

        self.booking3 = Booking.objects.create(
            date=datetime.date(2022, 3, 20),
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

    # Test the TimeSlotForm clean_time method for an invalid early time after 5pm.
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
        self.assertEqual(form.errors['first_name'][0], 'This field is required.')

    # Test that the CustomSignUpForm last name field is required. 
    def test_customsignupform_last_name_field_is_required(self):
        form = CustomSignUpForm({'last_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors.keys())
        self.assertEqual(form.errors['last_name'][0], 'This field is required.')
    
    # Test that the CustomSignUpForm first name field must be letters only.
    def test_customsignupform_first_name_field_is_letters(self):
        form = CustomSignUpForm({'first_name': '11112222abc'})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.keys())
        self.assertEqual(form.errors['first_name'][0], 'Only letters are allowed.')

    # Test that the CustomSignUpForm last name field must be letters only.
    def test_customsignupform_last_name_field_is_letters(self):
        form = CustomSignUpForm({'last_name': '11112222abc'})
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors.keys())
        self.assertEqual(form.errors['last_name'][0], 'Only letters are allowed.')

    # Test that the CustomSignUpForm first name widget is a TextField.
    def test_customsignupform_first_name_widget_is_textfield(self):
        form = CustomSignUpForm()
        self.assertEqual(form.fields['first_name'].widget.__class__.__name__, 'TextInput')

    # Test that the CustomSignUpForm last name widget is a TextField.
    def test_customsignupform_last_name_widget_is_textfield(self):
        form = CustomSignUpForm()
        self.assertEqual(form.fields['last_name'].widget.__class__.__name__, 'TextInput')

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
        self.assertEqual(form.errors['party_size'][0], 'This field is required.')

    # Test that BookingForm time slot field is required. 
    def test_bookingform_time_slot_field_is_required(self):
        form = BookingForm(user=self.user1, data={'time_slot': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('time_slot', form.errors.keys())
        self.assertEqual(form.errors['time_slot'][0], 'This field is required.')

    # Test that the date, party size and time slot fields are named as explicit
    # fields in the BookingForm.
    def test_fields_are_explicit_in_bookingform_metaclass(self):
        form = BookingForm(user=self.user1)
        self.assertEqual(form.Meta.fields, ('date', 'party_size', 'time_slot'))

    # Test that the BookingForm party size widget is a Select.
    def test_bookingform_party_size_widget_is_select(self):
        form = BookingForm(user=self.user1)
        self.assertEqual(form.fields['party_size'].widget.__class__.__name__, 'Select')

    # Test that the BookingForm date widget is readonly.
    def test_bookingform_date_widget_is_readonly(self):
        form = BookingForm(user=self.user1)
        self.assertTrue(form.fields['date'].widget.attrs['readonly'])
    