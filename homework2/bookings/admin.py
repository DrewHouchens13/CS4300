from django.contrib import admin
from .models import Movie, Seat, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'showtime', 'release_date', 'duration']
    list_filter = ['showtime', 'release_date']
    search_fields = ['title', 'description']
    ordering = ['-showtime']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_number']
    search_fields = ['seat_number']
    ordering = ['seat_number']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'seat', 'user', 'booking_date']
    list_filter = ['movie', 'booking_date']
    search_fields = ['movie__title', 'user__username', 'seat__seat_number']
    ordering = ['-booking_date']