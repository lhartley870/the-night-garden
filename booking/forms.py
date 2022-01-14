from django import forms
from django.core.exceptions import ValidationError
from .models import TimeSlot


class TimeSlotForm(forms.ModelForm):

    class Meta:
        model = TimeSlot
        fields = ('time', 'tables')

    def clean_time(self):
        """
        Method to add validation when an Admin user is adding/editing time
        slots to ensure that slots are not added before the restaurant opens at
        17:30 or after 22:00 (to allow enough time between the last booking
        slot and the restaurant closing at midnight).
        """
        # Code for this method was adapted from a question posted by Amistad
        # and an answer given by Daniel Roseman on this Stack Overflow post -
        # https://stackoverflow.com/questions/24802244/custom-validation-in-django-admin
        time = self.cleaned_data.get('time')
        too_early = time.hour < 17 or time.hour == 17 and time.minute < 30
        too_late = time.hour > 22 or time.hour == 22 and time.minute > 00
        if (too_early or too_late):
            raise ValidationError('Time slots must be between 17:30 and 22:00')
        else:
            return self.cleaned_data['time']
