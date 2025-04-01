from django.contrib import admin
from django.urls import path, include
from AIRPORT_MANAGER.views.flights import FlightViewSet
from rest_framework.routers import DefaultRouter
from AIRPORT_MANAGER.views.crewFlightSet import MyCrewFlightsViewSet
router = DefaultRouter()
router.register(r'flights', FlightViewSet, basename='flights')

router.register(r'my-crew-flights', MyCrewFlightsViewSet, basename='my-crew-flights')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
