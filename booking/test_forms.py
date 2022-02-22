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
