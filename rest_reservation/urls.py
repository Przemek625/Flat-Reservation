from django.conf.urls import url

from rest_reservation import views

urlpatterns = [
    url(r'^rest_reservation/list_cities$', views.CitiesList.as_view()),
    url(r'^rest_reservation/list_flats$', views.FlatsList.as_view()),
    url(r'^rest_reservation/list_reservations$', views.ReservationsList.as_view()),
    url(r'^rest_reservation/search/$', views.SearchFlatResults.as_view()),
]
