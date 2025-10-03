from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Movie, Seat, Booking

User = get_user_model()

def _ensure_seat_grid(rows: int = 5, cols: int = 5) -> None:
    """Create a consistent Rows x Cols seat grid (e.g., A1..E5) if no seats exist."""
    if Seat.objects.exists():
        return
    row_letters = [chr(ord('A') + i) for i in range(rows)]
    to_create = []
    for r in row_letters:
        for c in range(1, cols + 1):
            to_create.append(Seat(seat_number=f"{r}{c}"))
    Seat.objects.bulk_create(to_create)

def movie_list_page(request):
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movie_list.html", {"movies": movies})

def seat_list_page(request):
    _ensure_seat_grid()
    seats = Seat.objects.all().order_by("seat_number")
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/seat_list.html", {"seats": seats, "movies": movies})

@require_http_methods(["POST"])
def quick_book_seat(request, seat_id):
    seat = get_object_or_404(Seat, pk=seat_id)
    movie_id = request.POST.get("movie_id")
    if not movie_id:
        return redirect("seat_list_page")
    movie = get_object_or_404(Movie, pk=movie_id)
    # Prevent double-booking for the same movie
    if Booking.objects.filter(movie=movie, seat=seat).exists():
        return redirect("seat_list_page")
    user = request.user if request.user.is_authenticated else User.objects.get_or_create(username="guest")[0]
    Booking.objects.create(movie=movie, seat=seat, user=user)
    messages.success(request, f"Successfully booked seat {seat.seat_number} for {movie.title}!")
    return redirect("movie_list_page")


def movie_seat_grid_page(request, movie_id: int):
    """Display a selectable seat grid for a specific movie; support multi-seat booking."""
    _ensure_seat_grid()
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        seat_ids = request.POST.getlist("seat_ids")
        user = request.user if request.user.is_authenticated else User.objects.get_or_create(username="guest")[0]
        booked_seats = []
        for sid in seat_ids:
            try:
                seat = Seat.objects.get(pk=sid)
            except Seat.DoesNotExist:
                continue
            if not Booking.objects.filter(movie=movie, seat=seat).exists():
                Booking.objects.create(movie=movie, seat=seat, user=user)
                booked_seats.append(seat.seat_number)
        if booked_seats:
            messages.success(request, f"Successfully booked seats {', '.join(booked_seats)} for {movie.title}!")
        return redirect("movie_list_page")

    seats = list(Seat.objects.all().order_by("seat_number"))
    booked_ids = set(Booking.objects.filter(movie=movie).values_list("seat_id", flat=True))
    # Group seats by row letter (first character) and sort by numeric column
    row_map = {}
    for s in seats:
        row = s.seat_number[0]
        try:
            col = int(s.seat_number[1:])
        except ValueError:
            col = 0
        row_map.setdefault(row, []).append((col, s))
    for r in row_map:
        row_map[r].sort(key=lambda t: t[0])
    ordered_rows = sorted(row_map.items(), key=lambda t: t[0])
    context = {
        "movie": movie,
        "ordered_rows": ordered_rows,
        "booked_ids": booked_ids,
    }
    return render(request, "bookings/seat_grid.html", context)

def booking_history_page(request):
    # If authenticated, show only their bookings; else show all (dev)
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user).select_related("movie", "seat").order_by("-booking_date")
    else:
        bookings = Booking.objects.select_related("movie", "seat", "user").order_by("-booking_date")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})
