from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
from pandas import date_range


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)
    postal_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Flat(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=255)
    flat_number = models.CharField(max_length=255)
    available_from = models.DateField()
    available_to = models.DateField()

    def __str__(self):
        return '%s %s %s %s' % \
               (self.city, self.street, self.street_number, self.flat_number)

    @staticmethod
    def display_available_flats(city, rsd, red):
        return Flat.objects.filter(city__name=city). \
            filter(available_from__lte=rsd, available_to__gte=red)

    @staticmethod
    def check__if_flat_is_available(rsd, red, flat_id):
        return Flat.objects. \
            filter(available_from__lte=rsd, available_to__gte=red).get(pk=flat_id)


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
    flat = models.ForeignKey(Flat, null=True, related_name='reservations')

    def __str__(self):
        return 'Reservation for flat in: %s from %s to %s' % \
               (self.flat, self.reservation_start_date, self.reservation_end_date)

    @staticmethod
    def list_unavailable_reservations(rsd, red):
        return Reservation.objects. \
            filter(Q(reservation_start_date__lte=rsd,
                     reservation_end_date__gte=rsd) |
                   Q(reservation_start_date__lte=red,
                     reservation_end_date__gte=red) |
                   Q(reservation_start_date__gte=rsd,
                     reservation_end_date__lte=red) |
                   Q(reservation_start_date__gte=rsd,
                     reservation_end_date__lte=red))

    @staticmethod
    def check_if_flat_is_reserved(flat_id, rsd, red):
        return Reservation.objects.filter(flat__id=flat_id). \
            filter(Q(reservation_start_date__lte=rsd,
                     reservation_end_date__gte=rsd) |
                   Q(reservation_start_date__lte=red,
                     reservation_end_date__gte=red) |
                   Q(reservation_start_date__gte=rsd,
                     reservation_end_date__lte=red) |
                   Q(reservation_start_date__gte=rsd,
                     reservation_end_date__lte=red))

    @staticmethod
    def reservation_list_for_flat(flat):
        reservations = Reservation.objects.filter(flat=flat)
        list_of_dates_when_flat_is_reserved = []
        for x in reservations:
            list_of_dates_when_flat_is_reserved.extend(
                [e.strftime("%Y-%m-%d") for e in
                 date_range(x.reservation_start_date, x.reservation_end_date, freq='D')])
        return list_of_dates_when_flat_is_reserved
