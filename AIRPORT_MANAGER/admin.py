from django.contrib import admin
from AIRPORT_MANAGER.models import (
    UserRole,
    CrewRole,
    User,
    Airport,
    Airline,
    Aircraft,
    Crew,
    CrewMember,
    Stopover,
    Flight,
    FlightCrew,
)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(CrewRole)
class CrewRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role')
    search_fields = ('name', 'email')
    list_filter = ('role',)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'country')
    search_fields = ('name', 'city', 'country')


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name', 'country')


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'capacity')
    search_fields = ('type',)


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ('crew_id',)


@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role', 'crew')
    list_filter = ('role',)
    search_fields = ('name',)


@admin.register(Stopover)
class StopoverAdmin(admin.ModelAdmin):
    list_display = ('stop_id', 'airport')


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_time', 'arrival_time', 'airline', 'status')
    list_filter = ('flight_type', 'status', 'airline')
    search_fields = ('flight_number',)


@admin.register(FlightCrew)
class FlightCrewAdmin(admin.ModelAdmin):
    list_display = ('flight', 'member')
    list_filter = ('flight',)
