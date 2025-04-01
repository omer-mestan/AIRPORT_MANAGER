from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta

from AIRPORT_MANAGER.models import Flight, Airport

class FlightSearchAPITest(TestCase):
    def setUp(self):
        self.airport_from = Airport.objects.create(name="Sofia Airport", city="Sofia", country="Bulgaria")
        self.airport_to = Airport.objects.create(name="London Heathrow", city="London", country="UK")

        # Полет с точни данни
        self.flight1 = Flight.objects.create(
            flight_number="BG123",
            departure_time=now() + timedelta(hours=5),
            arrival_time=now() + timedelta(hours=8),
            duration=timedelta(hours=3),
            price=250.00,
            flight_type="Passenger",
            status="On Time",
            from_airport=self.airport_from,
            to_airport=self.airport_to
        )

        # Полет без дестинация "Atlantis"
        self.flight2 = Flight.objects.create(
            flight_number="BG200",
            departure_time=now() + timedelta(hours=1),
            arrival_time=now() + timedelta(hours=3),
            duration=timedelta(hours=2),
            price=180.00,
            flight_type="Passenger",
            status="Delayed",
            from_airport=self.airport_from,
            to_airport=self.airport_to
        )

        self.client = APIClient()

    def test_search_by_destination(self):
        response = self.client.get("/api/flights/?destination=London")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn("flight_number", response.data[0])

    def test_search_by_flight_number(self):
        response = self.client.get("/api/flights/?flight_number=BG123")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["flight_number"], "BG123")

    def test_search_with_invalid_destination(self):
        response = self.client.get("/api/flights/?destination=Atlantis")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    """def test_search_by_time_range(self):
        response = self.client.get("/api/flights/?departure_after=04:00&departure_before=23:00")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(f["flight_number"] == "HD528" for f in response.data))
    """