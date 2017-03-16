from django.conf.urls import url

from rest_reservation import views

urlpatterns = [
    url(r'^rest_reservation/list_cities$', views.list_cities),
    url(r'^rest_reservation/list_flats$', views.list_flats),
    url(r'^rest_reservation/list_reservations$', views.list_reservations),
]
