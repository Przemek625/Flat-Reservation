from rest_framework import generics
from rest_framework.response import Response

from reservation.models import City, Flat, Reservation
from rest_reservation.serializers import CitySerializer, FlatSerializer, ReservationSerializer


class CitiesList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class ReservationsList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class FlatsList(generics.ListCreateAPIView):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer


class SearchFlatResults(generics.ListAPIView):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer

    def list(self, request, *args, **kwargs):
        city = request.GET.get('city', '')
        rsd = request.GET.get('rsd', '')
        red = request.GET.get('red', '')

        available_flats = self.get_queryset()
        available_flats = available_flats.filter(city=City.objects.filter(name=city),
                                                 available_from__lte=rsd, available_to__gte=red)
        unavailable_reservations = Reservation.list_unavailable_reservations(rsd, red)
        unavailable_flats_pk_set = [e.flat.pk for e in unavailable_reservations]
        available_flats = available_flats.exclude(pk__in=unavailable_flats_pk_set)
        serializer = FlatSerializer(available_flats, many=True)

        return Response(serializer.data)
