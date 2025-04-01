from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model

from AIRPORT_MANAGER.models import (
    Airport, Flight, Crew, CrewRole, CrewMember, FlightCrew
)

User = get_user_model()

class FlightSearchAndCrewViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Airports
        self.airport_from = Airport.objects.create(name="Sofia Airport", city="Sofia", country="BG")
        self.airport_to = Airport.objects.create(name="London Airport", city="London", country="UK")

        # Flight BG123
        self.flight = Flight.objects.create(
            flight_number="BG123",
            departure_time=now().replace(hour=12, minute=0, second=0),
            arrival_time=now().replace(hour=15, minute=0, second=0),
            duration=timedelta(hours=3),
            price=150.00,
            flight_type="Passenger",
            status="On Time",
            from_airport=self.airport_from,
            to_airport=self.airport_to
        )

        # Another flight (to be shown on empty query)
        self.flight2 = Flight.objects.create(
            flight_number="BG999",
            departure_time=now() + timedelta(days=1),
            arrival_time=now() + timedelta(days=1, hours=2),
            duration=timedelta(hours=2),
            price=120.00,
            flight_type="Passenger",
            status="Delayed",
            from_airport=self.airport_from,
            to_airport=self.airport_to
        )

    def test_search_valid_criteria(self):
        response = self.client.get("/api/flights/", {
            "destination": "London",
            "flight_number": "BG123",
            "departure_after": "10:00",
            "departure_before": "16:00"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        flight = response.data[0]
        self.assertEqual(flight["flight_number"], "BG123")
        self.assertIn("status", flight)

    def test_search_invalid_destination(self):
        response = self.client.get("/api/flights/?destination=Atlantis")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_search_empty_criteria_returns_all(self):
        response = self.client.get("/api/flights/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_crew_member_sees_future_flights(self):
        user = User.objects.create_user(username="crewman", password="test123")
        role = CrewRole.objects.create(name="Pilot")
        crew = Crew.objects.create()
        member = CrewMember.objects.create(user=user, name="Crewman Ivan", role=role, crew=crew)
        FlightCrew.objects.create(flight=self.flight2, member=member)

        self.client.force_authenticate(user=user)
        response = self.client.get("/api/my-crew-flights/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["flight_number"], "BG999")
        self.assertEqual(len(response.data[0]["crew"]), 1)
        self.assertEqual(response.data[0]["crew"][0]["name"], "Crewman Ivan")

    def test_non_crew_member_access_denied(self):
        user = User.objects.create_user(username="notcrew", password="test123")
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/my-crew-flights/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_crew_member_with_no_flights(self):
        user = User.objects.create_user(username="emptycrew", password="test123")
        role = CrewRole.objects.create(name="Engineer")
        crew = Crew.objects.create()
        CrewMember.objects.create(user=user, name="Empty Crew", role=role, crew=crew)

        self.client.force_authenticate(user=user)
        response = self.client.get("/api/my-crew-flights/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])