from django.test import TestCase
from django.utils.timezone import now, timedelta
from rest_framework.test import APIClient
from rest_framework import status

from AIRPORT_MANAGER.models import (
    Flight, Airport, CrewMember, Crew, CrewRole, FlightCrew, User
)

class MyCrewFlightsAPITest(TestCase):
    def setUp(self):
        # Създаване на потребител
        self.user = User.objects.create(
            name="Ivan",
            email="ivan@example.com",
            password="pass1234"
        )

        # Свързан CrewMember
        self.crew_role = CrewRole.objects.create(name="Pilot")
        self.crew = Crew.objects.create()
        self.crew_member = CrewMember.objects.create(
            name="Ivan", role=self.crew_role, crew=self.crew, user=self.user
        )

        # Летища
        self.airport_from = Airport.objects.create(name="Sofia Airport", city="Sofia", country="Bulgaria")
        self.airport_to = Airport.objects.create(name="Berlin Airport", city="Berlin", country="Germany")

        # Полет
        self.flight = Flight.objects.create(
            flight_number="BG001",
            departure_time=now() + timedelta(hours=1),
            arrival_time=now() + timedelta(hours=3),
            duration=timedelta(hours=2),
            price=199.99,
            flight_type="Passenger",
            status="On Time",
            from_airport=self.airport_from,
            to_airport=self.airport_to
        )

        # Създаване на междинна връзка (FlightCrew)
        FlightCrew.objects.create(flight=self.flight, member=self.crew_member)

        # Аутентикация
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_my_crew_flights_list(self):
        response = self.client.get("/api/my-crew-flights/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['flight_number'], "BG001")
        self.assertIn("crew", response.data[0])
        self.assertEqual(response.data[0]["crew"][0]["name"], "Ivan")