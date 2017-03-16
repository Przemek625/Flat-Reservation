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






