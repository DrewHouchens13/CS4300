from rest_framework import serializers
from .models import Movie, Seat, Booking


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model, handles JSON conversion for API responses."""
    
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration", "showtime"]


class SeatSerializer(serializers.ModelSerializer):
    """Serializer for Seat model, handles JSON conversion for API responses."""
    
    class Meta:
        model = Seat
        fields = ["id", "seat_number"]


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model with nested movie and seat details.
    
    Uses nested serializers for read operations to provide full object details,
    and PrimaryKeyRelatedField for write operations to accept IDs.
    """
    # Nested serializers for read operations (GET)
    movie = MovieSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)
    
    # Primary key fields for write operations (POST/PUT)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source="movie", write_only=True
    )
    seat_id = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(), source="seat", write_only=True
    )

    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "user", "booking_date", "movie_id", "seat_id"]
        read_only_fields = ["user", "booking_date"]
