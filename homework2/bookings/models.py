from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    """
    Represents a movie available for booking.
    
    Attributes:
        title: The movie title
        description: Detailed description of the movie
        release_date: Original release date
        duration: Runtime in minutes
        showtime: Scheduled showing time (optional)
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    showtime = models.DateTimeField(help_text="Movie showtime", null=True, blank=True)

    def __str__(self):
        return self.title


class Seat(models.Model):
    """
    Represents a theater seat.
    
    Attributes:
        seat_number: Unique identifier for the seat (e.g., "A1", "B5")
    """
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"Seat {self.seat_number}"


class Booking(models.Model):
    """
    Represents a seat booking for a specific movie.
    
    A booking links a user, seat, and movie together. The unique constraint
    ensures that the same seat cannot be booked twice for the same movie,
    preventing double-booking. However, the same seat can be booked for
    different movies.
    
    Attributes:
        movie: The movie being booked
        seat: The seat being reserved
        user: The user making the booking
        booking_date: Timestamp when the booking was created
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent double-booking: same seat cannot be booked twice for the same movie
        constraints = [
            models.UniqueConstraint(fields=["movie", "seat"], name="unique_booking_per_movie_seat"),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.seat.seat_number})"
