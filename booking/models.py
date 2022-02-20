from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Table(models.Model):
    SIZE = [(2, 2), (4, 4), (6, 6), (8, 8)]
    name = models.CharField(max_length=15, unique=True)
    size = models.PositiveSmallIntegerField(choices=SIZE)

    class Meta:
        ordering = ['size']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Customised save method added to convert all table names
        to lowercase characters before being entered in the database.
        This prevents the same names with different uppercase and
        lowercase characters from getting around the requirement for
        the table name field to be 'unique'.
        """
        # Code for converting a model field to lowercase before
        # saving it in the database taken from an answer given
        # by Mattia on this Stack Overflow post -
        # https://stackoverflow.com/questions/48574940/how-do-you-
        # make-a-lowercase-field-in-a-django-model/48596135
        self.name = self.name.lower()
        return super(Table, self).save(*args, **kwargs)


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
