from django.contrib import admin

# Register your models here.
from reservation.models import City, Reservation, Flat

admin.site.register(City)
admin.site.register(Reservation)
admin.site.register(Flat)