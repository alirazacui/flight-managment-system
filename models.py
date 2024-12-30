from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model to include roles
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username



# Flight Model - Admin manages flights
class Flight(models.Model):
    flight_number = models.CharField(max_length=20, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    available_seats = models.IntegerField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number} - {self.origin} to {self.destination}"


# Booking Model - Customers can book flights
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Canceled', 'Canceled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    PNR = models.CharField(max_length=20, unique=True)
    total_tickets = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Booked')
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.PNR} by {self.customer.username}"


class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    id_card_number = models.CharField(max_length=20, null=True, blank=True)
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"Passenger {self.name} - Seat {self.seat_number}"
    
# Report Model - Admin can generate flight reports
class Report(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    total_bookings = models.IntegerField()
    available_seats = models.IntegerField()
    cancellations = models.IntegerField()

    def __str__(self):
        return f"Report for {self.flight.flight_number}"
    
