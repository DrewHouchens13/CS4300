from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

User = get_user_model()

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by("title")
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]  # dev-friendly


class SeatViewSet(viewsets.ModelViewSet):
    """
    /api/seats/                -> list/create
    /api/seats/?is_booked=false -> filter available seats
    /api/seats/<id>/book/      -> POST {movie_id: <id>} to book this seat
    """
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        is_booked = self.request.query_params.get("is_booked")
        if is_booked is not None:
            if is_booked.lower() in ("true", "1", "yes"):
                qs = qs.filter(is_booked=True)
            elif is_booked.lower() in ("false", "0", "no"):
                qs = qs.filter(is_booked=False)
        return qs

    @action(detail=True, methods=["post"])
    def book(self, request, pk=None):
        """
        Book this seat by creating a Booking and marking seat.is_booked=True.
        Expects JSON: {"movie_id": <id>}
        Uses authenticated user if available, else a 'guest' user for dev convenience.
        """
        seat = self.get_object()
        if seat.is_booked:
            return Response({"detail": "Seat already booked."}, status=400)

        movie_id = request.data.get("movie_id")
        if not movie_id:
            return Response({"detail": "movie_id is required."}, status=400)

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"detail": "Invalid movie_id."}, status=400)

        # Choose user: real user if logged in; else create/get a 'guest' user for dev
        user = request.user if request.user.is_authenticated else None
        if user is None:
            user, _ = User.objects.get_or_create(username="guest")

        booking = Booking.objects.create(movie=movie, seat=seat, user=user)
        seat.is_booked = True
        seat.save(update_fields=["is_booked"])

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingViewSet(viewsets.ModelViewSet):
    """
    /api/bookings/      -> list/create
    /api/bookings/<id>/ -> retrieve/update/delete
    GET can be filtered by ?user=me to show current user's bookings (if logged in)
    """
    queryset = Booking.objects.select_related("movie", "seat", "user").order_by("-booking_date")
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        # If you later enable auth, let users see only their own bookings via ?user=me
        if self.request.user.is_authenticated and self.request.query_params.get("user") == "me":
            qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        # If user is authenticated, use them; else fallback to 'guest' for dev
        user = self.request.user if self.request.user.is_authenticated else None
        if user is None:
            user, _ = User.objects.get_or_create(username="guest")
        serializer.save(user=user)