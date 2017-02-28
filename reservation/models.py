from __future__ import unicode_literals
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)
    postal_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Flat(models.Model):
    # TODO Dopisac od kiedy do kiedy mieszkanie jest dostepne i przez kogo zarezerwowane
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=255)
    flat_number = models.CharField(max_length=255)
    # available_from = models.DateField()
    # available_to = models.DateField()

    def __str__(self):
        return '%s %s %s %s' % \
               (self.city, self.street, self.street_number, self.flat_number)


class Reservation(models.Model):
    RESERVED = 0
    AVAILABLE = 1
    STATUS = (
        (RESERVED, "Reserved"),
        (AVAILABLE, "Available"),
    )
    status = models.IntegerField(choices=STATUS, default=AVAILABLE)
    reservation_start_date = models.DateField()
    reservation_end_date = models.DateField()
    reserved_by = models.CharField(max_length=255)
    flat = models.ForeignKey(Flat, null=True)

    def __str__(self):
        return 'Reservation for flat in: %s from %s to %s' % \
               (self.flat, self.reservation_start_date, self.reservation_end_date)


