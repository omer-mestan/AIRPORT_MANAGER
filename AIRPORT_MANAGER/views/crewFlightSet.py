from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from AIRPORT_MANAGER.models import Flight, CrewMember

class MyCrewFlightsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            crew_member = request.user.crew_profile
        except CrewMember.DoesNotExist:
            return Response({"detail": "Не сте свързан с екипажа."}, status=403)

        flights = Flight.objects.filter(
            crew_members=crew_member,
            departure_time__gte=now()
        ).prefetch_related('crew_members', 'from_airport', 'to_airport')

        results = []
        for flight in flights:
            results.append({
                "flight_number": flight.flight_number,
                "from": flight.from_airport.name if flight.from_airport else "",
                "to": flight.to_airport.name if flight.to_airport else "",
                "departure": flight.departure_time,
                "crew": [
                    {
                        "name": cm.name,
                        "role": cm.role.name if cm.role else "?"
                    }
                    for cm in flight.crew_members.all()
                ]
            })
        return Response(results)
