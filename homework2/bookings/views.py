from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

User = get_user_model()

class MovieViewSet(viewsets.ModelViewSet):
    """
    Movie Management API
    
    📋 List all movies: GET /api/movies/
    ➕ Create movie: POST /api/movies/ (use form at bottom)
    🔗 Quick links to each movie shown below
    
    On individual movie pages, scroll down for:
    🗑️ Delete Movie button
    🎬 Update Showtime form
    """
    queryset = Movie.objects.all().order_by("title")
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_renderer_context(self):
        """Add movies to template context for link generation"""
        context = super().get_renderer_context()
        if self.action == 'list':
            context['movie_list'] = list(self.get_queryset())
        return context

    @action(detail=True, methods=["post"], url_path='delete-movie', url_name='delete-movie')
    def delete_movie(self, request, pk=None):
        """
        Delete this movie and all associated bookings.
        """
        movie = self.get_object()
        movie_title = movie.title
        booking_count = Booking.objects.filter(movie=movie).count()
        movie.delete()
        return Response({
            "success": True,
            "message": f"✅ Movie '{movie_title}' deleted successfully!",
            "bookings_deleted": booking_count
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path='update-showtime', url_name='update-showtime')
    def update_showtime(self, request, pk=None):
        """
        Update the showtime for this movie.
        
        Required field:
        - showtime: ISO 8601 datetime (e.g., "2025-10-15T19:30:00Z")
        """
        movie = self.get_object()
        showtime = request.data.get("showtime")
        
        if not showtime:
            return Response({
                "error": "showtime field is required",
                "example": {"showtime": "2025-10-15T19:30:00Z"}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        movie.showtime = showtime
        movie.save()
        
        return Response({
            "success": True,
            "message": f"✅ Showtime updated for '{movie.title}'",
            "movie": MovieSerializer(movie).data
        }, status=status.HTTP_200_OK)


class SeatViewSet(viewsets.ModelViewSet):
    """
    Seat Management API
    """
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["post"])
    def book(self, request, pk=None):
        """
        Book this seat for a movie.
        Required: {"movie_id": <movie_id>}
        """
        seat = self.get_object()
        movie_id = request.data.get("movie_id")
        
        if not movie_id:
            return Response({"error": "movie_id is required"}, status=400)

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Invalid movie_id"}, status=400)

        if Booking.objects.filter(movie=movie, seat=seat).exists():
            return Response({"error": "Seat already booked for this movie"}, status=400)

        user = request.user if request.user.is_authenticated else None
        if user is None:
            user, _ = User.objects.get_or_create(username="guest")

        booking = Booking.objects.create(movie=movie, seat=seat, user=user)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingViewSet(viewsets.ModelViewSet):
    """
    Booking Management API
    """
    queryset = Booking.objects.select_related("movie", "seat", "user").order_by("-booking_date")
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated and self.request.query_params.get("user") == "me":
            qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        if user is None:
            user, _ = User.objects.get_or_create(username="guest")
        serializer.save(user=user)
