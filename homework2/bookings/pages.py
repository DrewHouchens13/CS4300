from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from .models import Movie, Seat, Booking

User = get_user_model()

def movie_list_page(request):
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movie_list.html", {"movies": movies})

def seat_list_page(request):
    seats = Seat.objects.all().order_by("seat_number")
    return render(request, "bookings/seat_list.html", {"seats": seats})

@require_http_methods(["POST"])
def quick_book_seat(request, seat_id):
    seat = get_object_or_404(Seat, pk=seat_id, is_booked=False)
    movie_id = request.POST.get("movie_id")
    if not movie_id:
        return redirect("seat_list_page")
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user if request.user.is_authenticated else User.objects.get_or_create(username="guest")[0]
    Booking.objects.create(movie=movie, seat=seat, user=user)
    seat.is_booked = True
    seat.save(update_fields=["is_booked"])
    return redirect("booking_history_page")

def booking_history_page(request):
    # If authenticated, show only their bookings; else show all (dev)
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user).select_related("movie", "seat").order_by("-booking_date")
    else:
        bookings = Booking.objects.select_related("movie", "seat", "user").order_by("-booking_date")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})
