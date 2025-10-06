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

    @action(detail=True, methods=["post"])
    def delete_movie(self, request, pk=None):
        """
        Delete a movie and all its bookings.
        POST to /api/movies/<id>/delete_movie/
        No body required.
        """
        movie = self.get_object()
        movie_title = movie.title
        movie.delete()
        return Response({
            "success": True,
            "message": f"Movie '{movie_title}' and all its bookings have been deleted."
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def update_showtime(self, request, pk=None):
        """
        Update the showtime for a movie.
        POST to /api/movies/<id>/update_showtime/
        Body: {"showtime": "2025-10-15T19:30:00Z"}
        """
        movie = self.get_object()
        showtime = request.data.get("showtime")
        
        if not showtime:
            return Response({
                "success": False,
                "error": "showtime field is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        movie.showtime = showtime
        movie.save()
        
        return Response({
            "success": True,
            "message": f"Showtime updated for '{movie.title}'",
            "movie": MovieSerializer(movie).data
        }, status=status.HTTP_200_OK)


class SeatViewSet(viewsets.ModelViewSet):
    """
    /api/seats/                -> list/create
    /api/seats/<id>/book/      -> POST {movie_id: <id>} to book this seat for a movie
    """
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["post"])
    def book(self, request, pk=None):
        """
        Book this seat for a given movie by creating a Booking.
        Expects JSON: {"movie_id": <id>}.
        Uses authenticated user if available, else a 'guest' user for dev convenience.
        """
        seat = self.get_object()

        movie_id = request.data.get("movie_id")
        if not movie_id:
            return Response({"detail": "movie_id is required."}, status=400)

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"detail": "Invalid movie_id."}, status=400)

        # If already booked for this movie, block
        if Booking.objects.filter(movie=movie, seat=seat).exists():
            return Response({"detail": "Seat already booked for this movie."}, status=400)

        # Choose user: real user if logged in; else create/get a 'guest' user for dev
        user = request.user if request.user.is_authenticated else None
        if user is None:
            user, _ = User.objects.get_or_create(username="guest")

        booking = Booking.objects.create(movie=movie, seat=seat, user=user)

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
