import datetime
from django.test import TestCase
from .forms import TimeSlotForm, CustomSignUpForm, BookingForm
from .models import Table, TimeSlot, Booking

# Create your tests here.
class TestForms(TestCase):

    def setUp(self):

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
