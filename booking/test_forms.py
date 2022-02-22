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
