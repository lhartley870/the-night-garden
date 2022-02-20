from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class NameField(models.CharField):
    """
    Special NameField class added to be used for name fields
    so that they are converted to lowercase characters before
    being entered in the database. This prevents the same names
    with different uppercase and lowercase characters from getting
    around any requirement for the name field to be 'unique'.
    """

    # Code for this NameField class taken from an answer given
    # by Danil and edited by Oran on this Stack Overflow post -
    # https://stackoverflow.com/questions/36330677/django-model
    # -set-default-charfield-in-lowercase
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Table(models.Model):
    SIZE = [(2, 2), (4, 4), (6, 6), (8, 8)]
    name = NameField(max_length=15, unique=True)
    size = models.PositiveSmallIntegerField(choices=SIZE)

    class Meta:
        ordering = ['size']

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    time = models.TimeField(unique=True)
    tables = models.ManyToManyField(Table, related_name='table_timeslots')

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.time.strftime("%H:%M")


class Booking(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    booker = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="booking")
    party_size = models.PositiveSmallIntegerField(
        "Number of Guests",
        validators=[
                    MinValueValidator(1),
                    MaxValueValidator(16)
        ]
    )
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE,
                                  related_name="time_slot_booking",
                                  verbose_name="Time")
    tables = models.ManyToManyField(Table, related_name='table_booking')
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']

    def __str__(self):
        date = self.date.strftime("%d %B %Y")
        return (
            f'Booking #{self.id} on {date} '
            f'for {self.party_size} guest(s) at {self.time_slot}'
        )

    def date_string(self):
        date = self.date.strftime("%d %B %Y")
        return date
