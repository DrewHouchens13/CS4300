# CS4300 - Movie Theater Booking Application

A RESTful Movie Theater Booking Application built with Django and Django REST Framework. This application allows users to view movies, book seats, and manage their booking history through both a REST API and an attractive web interface.

**🌐 Live Application:** [https://houchensticketing.onrender.com/api/pages/movies/](https://houchensticketing.onrender.com/api/pages/movies/)

---

## 📂 Project Structure

```
CS4300/
├── homework2/                          # Main Django project directory
│   ├── HouchensTicketingApp/          # Django project settings
│   │   ├── settings.py                # Configuration and settings
│   │   ├── urls.py                    # Root URL routing
│   │   ├── wsgi.py                    # WSGI configuration
│   │   └── asgi.py                    # ASGI configuration
│   ├── bookings/                      # Main Django app
│   │   ├── models.py                  # Movie, Seat, and Booking models
│   │   ├── views.py                   # API ViewSets (MovieViewSet, SeatViewSet, BookingViewSet)
│   │   ├── serializers.py             # DRF Serializers for JSON conversion
│   │   ├── pages.py                   # Django template views (MVT pattern)
│   │   ├── urls.py                    # App-specific URL routing
│   │   ├── tests.py                   # Unit and integration tests
│   │   ├── admin.py                   # Django admin configuration
│   │   ├── migrations/                # Database migrations
│   │   └── templates/                 # HTML templates
│   │       ├── bookings/
│   │       │   ├── base.html          # Bootstrap base template
│   │       │   ├── movie_list.html    # Movie listing page
│   │       │   ├── seat_booking.html  # Seat booking interface
│   │       │   └── booking_history.html # User booking history
│   │       └── rest_framework/
│   │           └── api.html           # Custom DRF browsable API template
│   ├── manage.py                      # Django management script
│   ├── requirements.txt               # Python dependencies
│   ├── build.sh                       # Render deployment script
│   └── db.sqlite3                     # SQLite database (development)
├── render.yaml                        # Render deployment configuration
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

---

## 🎯 Features

### RESTful API Endpoints

#### Movies API
- **`GET /api/movies/`** - List all movies
- **`POST /api/movies/`** - Create a new movie
- **`GET /api/movies/{id}/`** - View movie details
- **`PUT /api/movies/{id}/`** - Update movie
- **`DELETE /api/movies/{id}/`** - Delete movie
- **`POST /api/movies/{id}/update-showtime/`** - Update movie showtime

#### Seats API
- **`GET /api/seats/`** - List all seats
- **`POST /api/seats/`** - Create new seats
- **`GET /api/seats/{id}/`** - View seat details
- **`POST /api/seats/{id}/book/`** - Book a seat for a movie

#### Bookings API
- **`GET /api/bookings/`** - List all bookings
- **`POST /api/bookings/`** - Create a new booking
- **`GET /api/bookings/{id}/`** - View booking details
- **`DELETE /api/bookings/{id}/`** - Cancel a booking

### Web Interface (Django Templates)
- **`/api/pages/movies/`** - Browse available movies with showtime information
- **`/api/pages/movies/{id}/seats/`** - Interactive seat selection grid per movie
- **`/api/pages/history/`** - View all booking history

### Database Models

1. **Movie**: Stores movie information
   - `title` - Movie title
   - `description` - Movie description
   - `release_date` - Release date
   - `duration` - Duration in minutes
   - `showtime` - Scheduled showtime

2. **Seat**: Represents theater seats
   - `seat_number` - Unique seat identifier (e.g., "A1", "B5")

3. **Booking**: Links movies, seats, and users
   - `movie` - Foreign key to Movie
   - `seat` - Foreign key to Seat
   - `user` - Foreign key to User
   - `booking_date` - Auto-generated timestamp
   - **Unique constraint**: Same seat cannot be booked twice for the same movie

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd CS4300
```

#### 2. Create and Activate a Virtual Environment
```bash
# Create a new virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on Mac/Linux
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
cd homework2
pip install -r requirements.txt
```

#### 4. Run Database Migrations
```bash
python manage.py migrate
```

#### 5. Run the Development Server
```bash
# For local development
python manage.py runserver

# For DevEdu environment (accessible externally)
python manage.py runserver 0.0.0.0:3000
```

#### 6. Access the Application
- **Web Interface**: `http://localhost:8000/api/pages/movies/`
- **API Root**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`

---

## 🧪 Running Tests

The application includes comprehensive unit and integration tests covering:
- Model creation and validation
- Database constraints (unique booking per movie/seat)
- API endpoint functionality (GET, POST, PUT, DELETE)
- Template page rendering
- Booking logic and error handling

### Run All Tests
```bash
cd homework2
python manage.py test
```

### Run Specific Test Classes
```bash
# Model tests only
python manage.py test bookings.tests.ModelTests

# API tests only
python manage.py test bookings.tests.APITests

# Page/template tests only
python manage.py test bookings.tests.PageTests
```

### Run with Verbose Output
```bash
python manage.py test --verbosity=2
```

### Test Coverage
The test suite includes:
- **Unit Tests**: Model creation, validation, string representations
- **Integration Tests**: API endpoints, request/response validation, status codes
- **Constraint Tests**: Unique booking validation, duplicate prevention
- **Template Tests**: Page loading and content rendering

---

## 🌐 Deployment (Render)

This application is deployed on Render at:
**[https://houchensticketing.onrender.com/api/pages/movies/](https://houchensticketing.onrender.com/api/pages/movies/)**

### Deployment Configuration

The deployment uses the following files:

1. **`render.yaml`** - Render service configuration
2. **`build.sh`** - Build script that:
   - Installs dependencies from `requirements.txt`
   - Collects static files
   - Runs database migrations

3. **`requirements.txt`** - Production dependencies:
   - Django 4.2.11
   - djangorestframework 3.16.1
   - dj-database-url (PostgreSQL connection)
   - psycopg2-binary (PostgreSQL adapter)
   - gunicorn (WSGI server)
   - whitenoise (static file serving)

### Environment Variables (Render)
- `DATABASE_URL` - PostgreSQL connection string (auto-configured by Render)
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Includes Render domain

---

## 🎨 User Interface

The application features a modern, responsive UI built with:
- **Bootstrap 5** - For responsive grid layout and components
- **Custom CSS** - Enhanced styling with gradient backgrounds
- **Emoji Icons** - Visual indicators for movies, seats, and bookings
- **Interactive Elements** - Dynamic seat selection grid with color-coded availability

### Design Features
- Mobile-responsive layout
- Intuitive navigation
- Visual feedback for seat availability (green = available, red = booked)
- Clear call-to-action buttons
- Organized information hierarchy

---

## 📖 API Usage Examples

### View All Movies
```bash
curl https://houchensticketing.onrender.com/api/movies/
```

### Create a New Movie
```bash
curl -X POST https://houchensticketing.onrender.com/api/movies/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inception",
    "description": "A mind-bending thriller",
    "release_date": "2010-07-16",
    "duration": 148,
    "showtime": "2025-10-20T19:30:00Z"
  }'
```

### Book a Seat
```bash
curl -X POST https://houchensticketing.onrender.com/api/seats/1/book/ \
  -H "Content-Type: application/json" \
  -d '{"movie_id": 1}'
```

### View Booking History
```bash
curl https://houchensticketing.onrender.com/api/bookings/
```

---

## 🛠️ Technology Stack

- **Backend Framework**: Django 4.2.11
- **API Framework**: Django REST Framework 3.16.1
- **Database**: 
  - SQLite (development)
  - PostgreSQL (production on Render)
- **Frontend**: HTML5, Bootstrap 5, Custom CSS
- **Deployment**: Render
- **Web Server**: Gunicorn (production)
- **Testing**: Django TestCase, DRF APITestCase

---

## 📝 Development Notes

### MVT Architecture
The application follows Django's Model-View-Template pattern:
- **Models** (`models.py`): Define database schema for Movie, Seat, Booking
- **Views** (`views.py`): API ViewSets handle CRUD operations
- **Templates** (`templates/`): HTML pages for user interface
- **Pages** (`pages.py`): Template views for MVT pattern

### REST API Design
- Uses Django REST Framework's ViewSets for consistent API structure
- Implements proper HTTP methods (GET, POST, PUT, DELETE)
- Returns appropriate status codes (200, 201, 400, 404)
- Provides browsable API interface for testing

### Database Constraints
- **Unique constraint** on `(movie, seat)` prevents double-booking
- Same seat can be booked for different movies
- Automatic timestamp tracking for bookings

---

## 👤 Developer

**Drew Houchens**

Created for CS4300 - Homework 2

---

## 📄 License

This project is for educational purposes as part of CS4300 coursework.

---

## 🔗 Quick Links

- **Live Application**: [https://houchensticketing.onrender.com/api/pages/movies/](https://houchensticketing.onrender.com/api/pages/movies/)
- **API Root**: [https://houchensticketing.onrender.com/api/](https://houchensticketing.onrender.com/api/)
- **Assignment PDF**: [https://tghastings.github.io/cs4300andcs5300/homework_2.pdf](https://tghastings.github.io/cs4300andcs5300/homework_2.pdf)
