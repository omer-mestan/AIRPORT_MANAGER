from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# ----------- USER ROLE -----------
class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# ----------- CREW ROLE -----------
class CrewRole(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# ----------- USER MODEL -----------
class User(AbstractUser):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username


# ----------- AIRPORT -----------
class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.city})"


# ----------- AIRLINE -----------
class Airline(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ----------- AIRCRAFT -----------
class Aircraft(models.Model):
    type = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.type} ({self.capacity} seats)"


# ----------- CREW -----------
class Crew(models.Model):
    crew_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Crew {self.crew_id}"


# ----------- CREW MEMBER -----------
class CrewMember(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='crew_profile'
    )
    name = models.CharField(max_length=100)
    role = models.ForeignKey(CrewRole, on_delete=models.SET_NULL, null=True)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name="members")

    def __str__(self):
        return f"{self.name} ({self.role.name if self.role else 'No Role'})"


# ----------- STOPOVER -----------
class Stopover(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    stop_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Stopover at {self.airport.name}"


# ----------- FLIGHT -----------
class Flight(models.Model):
    flight_number = models.CharField(max_length=20, unique=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    flight_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    crew = models.ForeignKey(Crew, on_delete=models.SET_NULL, null=True)
    airline = models.ForeignKey(Airline, on_delete=models.SET_NULL, null=True)
    stopover = models.ForeignKey(Stopover, on_delete=models.SET_NULL, null=True)

    from_airport = models.ForeignKey(
        Airport, on_delete=models.SET_NULL, null=True, related_name='departures'
    )
    to_airport = models.ForeignKey(
        Airport, on_delete=models.SET_NULL, null=True, related_name='arrivals'
    )

    users = models.ManyToManyField(User, related_name='booked_flights')  # search/book/view
    crew_members = models.ManyToManyField(
        CrewMember, through='FlightCrew', related_name='flights'
    )

    def __str__(self):
        return self.flight_number


# ----------- FLIGHTCREW M2M THROUGH TABLE -----------
class FlightCrew(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    member = models.ForeignKey(CrewMember, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('flight', 'member')

    def __str__(self):
        return f"{self.member.name} assigned to {self.flight.flight_number}"
