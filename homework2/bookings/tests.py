from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from .models import Movie, Seat, Booking


class ModelTests(TestCase):
    """Unit tests for Movie, Seat, and Booking models"""
    
    def setUp(self):
        """Set up test data"""
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="A test movie description",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.seat = Seat.objects.create(seat_number="A1")
        self.user = User.objects.create_user(username="testuser", password="testpass")
    
    def test_movie_creation(self):
        """Test Movie model creation and string representation"""
        self.assertEqual(str(self.movie), "Test Movie")
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.duration, 120)
        self.assertEqual(self.movie.release_date, date(2024, 1, 1))
    
    def test_seat_creation(self):
        """Test Seat model creation and string representation"""
        self.assertEqual(str(self.seat), "Seat A1")
        self.assertEqual(self.seat.seat_number, "A1")
    
    def test_booking_creation(self):
        """Test Booking model creation and string representation"""
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        expected_str = f"{self.user.username} - {self.movie.title} ({self.seat.seat_number})"
        self.assertEqual(str(booking), expected_str)
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat)
        self.assertEqual(booking.user, self.user)
    
    def test_booking_unique_constraint(self):
        """Test that same seat cannot be booked twice for same movie"""
        # Create first booking
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        
        # Try to create duplicate booking - should raise IntegrityError
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
    
    def test_seat_can_be_booked_for_different_movies(self):
        """Test that same seat can be booked for different movies"""
        movie2 = Movie.objects.create(
            title="Another Movie",
            description="Another test movie",
            release_date=date(2024, 2, 1),
            duration=90
        )
        
        # Book same seat for two different movies
        booking1 = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        booking2 = Booking.objects.create(movie=movie2, seat=self.seat, user=self.user)
        
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(booking1.seat, booking2.seat)
        self.assertNotEqual(booking1.movie, booking2.movie)


class APITests(APITestCase):
    """Integration tests for API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.movie = Movie.objects.create(
            title="API Test Movie",
            description="A movie for API testing",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.seat = Seat.objects.create(seat_number="B2")
        self.user = User.objects.create_user(username="apiuser", password="testpass")
    
    def test_movies_api_list(self):
        """Test GET /api/movies/ returns list of movies"""
        url = '/api/movies/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "API Test Movie")
        self.assertEqual(response.data[0]['duration'], 120)
    
    def test_movies_api_create(self):
        """Test POST /api/movies/ creates new movie"""
        url = '/api/movies/'
        data = {
            'title': 'New Movie',
            'description': 'A newly created movie',
            'release_date': '2024-03-01',
            'duration': 150
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Movie')
        self.assertEqual(Movie.objects.count(), 2)
    
    def test_movie_update_showtime(self):
        """Test POST /api/movies/{id}/update-showtime/ updates movie showtime"""
        url = f'/api/movies/{self.movie.pk}/update-showtime/'
        data = {'showtime': '2025-10-15T19:30:00Z'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('updated', response.data['message'].lower())
        
        # Verify movie was updated
        self.movie.refresh_from_db()
        self.assertIsNotNone(self.movie.showtime)
    
    def test_movie_update_showtime_missing_data(self):
        """Test update showtime fails without showtime data"""
        url = f'/api/movies/{self.movie.pk}/update-showtime/'
        data = {}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_seats_api_list(self):
        """Test GET /api/seats/ returns list of seats"""
        url = '/api/seats/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['seat_number'], "B2")
    
    def test_seats_api_create(self):
        """Test POST /api/seats/ creates new seat"""
        url = '/api/seats/'
        data = {'seat_number': 'C3'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['seat_number'], 'C3')
        self.assertEqual(Seat.objects.count(), 2)
    
    def test_seat_booking_api(self):
        """Test POST /api/seats/{id}/book/ books a seat"""
        url = f'/api/seats/{self.seat.pk}/book/'
        data = {'movie_id': self.movie.pk}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        
        booking = Booking.objects.first()
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat)
    
    def test_seat_booking_duplicate_fails(self):
        """Test that booking same seat twice for same movie fails"""
        # Create first booking
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        
        # Try to book again
        url = f'/api/seats/{self.seat.pk}/book/'
        data = {'movie_id': self.movie.pk}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already booked', response.data['error'].lower())
    
    def test_bookings_api_list(self):
        """Test GET /api/bookings/ returns list of bookings"""
        # Create a booking first
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        
        url = '/api/bookings/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['movie']['title'], "API Test Movie")
        self.assertEqual(response.data[0]['seat']['seat_number'], "B2")
    
    def test_bookings_api_create(self):
        """Test POST /api/bookings/ creates new booking"""
        url = '/api/bookings/'
        data = {
            'movie_id': self.movie.pk,
            'seat_id': self.seat.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        
        booking = Booking.objects.first()
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat)


class PageTests(TestCase):
    """Tests for Django template pages"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.movie = Movie.objects.create(
            title="Page Test Movie",
            description="A movie for page testing",
            release_date=date(2024, 1, 1),
            duration=120
        )
    
    def test_movie_list_page(self):
        """Test movie list page loads correctly"""
        url = '/api/pages/movies/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Page Test Movie")
    
    def test_seat_booking_page(self):
        """Test seat booking page loads correctly"""
        url = f'/api/pages/movies/{self.movie.pk}/seats/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Page Test Movie")
    
    def test_booking_history_page(self):
        """Test booking history page loads correctly"""
        url = '/api/pages/history/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)