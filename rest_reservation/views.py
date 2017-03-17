from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from reservation.models import City, Flat, Reservation
from rest_reservation.serializers import CitySerializer, FlatSerializer, ReservationSerializer


@api_view(['GET', 'POST'])
def list_cities(request):

    if request.method == 'GET':
        serializer = CitySerializer(City.objects.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def list_flats(request):

    if request.method == 'GET':
        serializer = FlatSerializer(Flat.objects.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FlatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def list_reservations(request):

    if request.method == 'GET':
        serializer = ReservationSerializer(Reservation.objects.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def list_search_flat_results(request):

    rsd = request.data['rsd']
    red = request.data['red']
    city = request.data['city']
    available_flats = Flat.display_available_flats(
        city, rsd, red)
    unavailable_reservations = Reservation.list_unavailable_reservations(rsd, red)
    unavailable_flats_pk_set = [e.flat.pk for e in unavailable_reservations]

    available_flats = available_flats.exclude(pk__in=unavailable_flats_pk_set)
    serializer = FlatSerializer(available_flats, many=True)

    if available_flats:
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)









