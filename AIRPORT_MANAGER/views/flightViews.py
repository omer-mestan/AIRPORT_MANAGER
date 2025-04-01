from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from AIRPORT_MANAGER.models import Flight
from AIRPORT_MANAGER.serializers import FlightSerializer
from AIRPORT_MANAGER.permissions import IsAdminOrInspectorForWrite

#Търсене на полети по дестинация и дата
class SearchFlightsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]
    queryset = Flight.objects.select_related('to_airport', 'from_airport', 'airline')
    filter_backends = [filters.SearchFilter]
    search_fields = ['to_airport__name', 'from_airport__name']

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params

        destination = params.get('destination')
        departure_date = params.get('departure_date')

        if destination:
            queryset = queryset.filter(to_airport__name__icontains=destination)
        if departure_date:
            queryset = queryset.filter(departure_time__date=departure_date)

        return queryset

#Преглед и редактиране на детайли за полет
class ManageFlightsViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInspectorForWrite]
    queryset = Flight.objects.select_related('to_airport', 'from_airport', 'airline')

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
