from django.db import models


# Create your models here.
class Table(models.Model):
    SIZE = [(2, 2), (4, 4), (6, 6), (8, 8)]
    name = models.CharField(max_length=15, unique=True)
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
