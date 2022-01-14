from django.db import models


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
