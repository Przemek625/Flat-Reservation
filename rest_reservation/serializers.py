from rest_framework import serializers
from reservation.models import Flat, City, Reservation


class ReservationSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        reservations = Reservation.check_if_flat_is_reserved(
            flat_id=attrs['flat'].id,
            rsd=attrs['reservation_start_date'],
            red=attrs['reservation_end_date']
        )

        if reservations:
            message = 'This Flat has been already reserved for given time frame'
            raise serializers.ValidationError(message)
        return super(ReservationSerializer, self).validate(attrs)

    class Meta:
        model = Reservation
        fields = '__all__'


class NestedReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('reservation_start_date', 'reservation_end_date')


class FlatSerializer(serializers.ModelSerializer):
    reservations = NestedReservationSerializer(many=True, required=False)

    class Meta:
        model = Flat
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name', 'postal_code')
