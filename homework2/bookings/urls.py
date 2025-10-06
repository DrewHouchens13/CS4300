from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet
from . import pages

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    # API
    path("", include(router.urls)),

    # Pages (MVT)
    path("pages/movies/", pages.movie_list_page, name="movie_list_page"),
    path("pages/history/", pages.booking_history_page, name="booking_history_page"),
    path("pages/movies/<int:movie_id>/seats/", pages.movie_seat_grid_page, name="movie_seat_grid_page"),
]
