from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from .models import Flight, Booking, Passenger

from django.contrib.auth.decorators import login_required  # Import all relevant models here

import random
import string  # Keep only if used for generating unique PNRs
from django.db import transaction


# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'airline_app/home.html')
  # Render the homepage template





 # Get the custom User model

 # Use this to get the custom user model

  # This fetches the custom User model


User = get_user_model()



def register_user(request):
    if request.method == "POST":
        # Get form data
        full_name = request.POST.get("full-name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        # Validate form data
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "airline_app/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, "airline_app/register.html")

        try:
            # Create a new user
            user = User.objects.create(
                username=email,
                email=email,
                first_name=full_name.split()[0],  # First name
                last_name=" ".join(full_name.split()[1:]),  # Last name
                phone=phone,
                address=address,
                role="Customer",
            )
            user.set_password(password)  # Hash the password
            user.save()

            messages.success(request, "Registration successful!")
            return redirect("login")  # Update with your login page URL
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return render(request, "airline_app/register.html")

    return render(request, "airline_app/register.html")



def customer_dashboard(request):
    return render(request, 'airline_app/customer_dashboard.html')

def admin_dashboard(request):
    return render(request, 'airline_app/admin_dashboard.html')





def user_login(request):
    next_page = request.GET.get('next')  # Get the 'next' parameter to redirect after login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user using the custom User model
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login the user
            auth_login(request, user)
            
            # Redirect to the appropriate page, or 'next' page if provided
            return redirect(next_page if next_page else 'customer_dashboard')
        else:
            # Add an error message if login fails
            messages.error(request, 'Invalid username or password')
            return render(request, 'airline_app/home.html')
    else:
        return render(request, 'airline_app/home.html')
# cnvkm h h  h dc h  hh   dd sdf  asfj dbhdf hyh by  hbyu  sdy nsdbd bhgn asadaskndasdn asdna  assd sdf    s   sdf   sdf   



def customer_booking(request):
    return render(request, 'airline_app/customer_bookings.html')


def adding_flight(request):
    if request.method == "POST":
        # Fetch data from the submitted form
        flight_number = request.POST.get('flight_number')
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        available_seats = request.POST.get('available_seats')
        fare = request.POST.get('fare')

        try:
            # Convert datetime inputs to proper formats
            departure_time = timezone.datetime.fromisoformat(departure_time)
            arrival_time = timezone.datetime.fromisoformat(arrival_time)

            # Create a new Flight object and save it
            Flight.objects.create(
                flight_number=flight_number,
                origin=origin,
                destination=destination,
                departure_time=departure_time,
                arrival_time=arrival_time,
                available_seats=int(available_seats),
                fare=float(fare),
            )

            # Success message
            messages.success(request, "Flight added successfully!")
            return redirect('add_flight')  # Redirect to the same page or another

        except Exception as e:
            # Error message
            messages.error(request, f"Error adding flight: {e}")
            return redirect('add_flight')  # Reload the form page

    # Render the form template
    return render(request, 'airline_app/add_flight.html')


def search_flights(request):
    flights = None  # Default: No flights found

    if request.method == "GET" and 'origin' in request.GET:
        # Retrieve form data from GET request
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        date = request.GET.get('date')

        try:
            # Parse the date input
            search_date = parse_date(date)

            # Query the database with search criteria
            flights = Flight.objects.filter(
                origin__iexact=origin,          # Case-insensitive match for origin
                destination__iexact=destination, # Case-insensitive match for destination
                 # Match only the date part of departure_time
            )

            # Optionally handle when no flights are found
            if not flights.exists():
                flights = None  # No flights match the criteria

        except Exception as e:
            print(f"Error: {e}")  # Log any parsing or query errors

    # Pass the search results to the template
    return render(request, 'airline_app/customer_bookings.html', {'flights': flights})



def generate_unique_pnr():
    while True:
        pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Booking.objects.filter(PNR=pnr).exists():
            return pnr

def book_flight(request, flight_id):
    """
    Handles booking a flight with robust seat assignment.
    """
    print(f"book_flight view called with flight_id: {flight_id}")
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == "POST":
        customer = request.user
        num_passengers = int(request.POST.get("num_passengers"))

        if num_passengers > flight.available_seats:
            messages.error(request, "Not enough seats available on this flight.")
            return redirect("flight_details", flight_id=flight_id)

        try:
            with transaction.atomic():
                pnr = generate_unique_pnr()
                booking = Booking.objects.create(
                    customer=customer,
                    flight=flight,
                    PNR=pnr,
                    total_tickets=num_passengers,
                )
                print(f"Booking created successfully with ID: {booking.id} and PNR: {booking.PNR}")

                # Lock Passenger records to avoid race conditions
                occupied_seats = list(
                    Passenger.objects.filter(booking__flight=flight)
                    .select_for_update()
                    .values_list("seat_number", flat=True)
                )
                print("Occupied seats at the start:", occupied_seats)

                next_seat = 1
                for _ in range(num_passengers):
                    # Assign the next available seat
                    while next_seat in occupied_seats:
                        next_seat += 1
                    occupied_seats.append(next_seat)  # Mark the seat as occupied

                    Passenger.objects.create(
                        booking=booking,
                        name=request.POST.get(f"passenger_name_{_}"),
                        passport_number=request.POST.get(f"passport_no_{_}"),
                        id_card_number=request.POST.get(f"id_card_no_{_}"),
                        seat_number=next_seat,
                    )
                    print(f"Passenger {_ + 1}: Assigned Seat={next_seat}")

                # Update flight availability
                flight.available_seats -= num_passengers
                flight.save()

            messages.success(request, f"Booking successful! Your PNR is {booking.PNR}.")
            return redirect("booking_success", booking_id=booking.id)

        except IntegrityError as e:
            print("IntegrityError occurred:", str(e))
            messages.error(request, "Error creating the booking. Please try again.")
            return redirect("search_flights")

        except Exception as e:
            print("Unexpected error occurred:", str(e))
            messages.error(request, "An unexpected error occurred. Please try again.")
            return redirect("search_flights")

    return render(request, "airline_app/booking_form.html", {"flight": flight})

def booking_success(request, booking_id):
    """
    Displays the booking success page.
    Debugging methods included to ensure booking data is retrieved correctly.
    """
    # Debugging: Log that the function is called
    print(f"booking_success view called with booking_id: {booking_id}")

    try:
        # Fetch the booking and passengers
        booking = Booking.objects.get(id=booking_id)
        passengers = Passenger.objects.filter(booking=booking)

        # Debugging: Log fetched data
        print(f"Booking details: PNR={booking.PNR}, Flight={booking.flight.flight_number}")
        print(f"Passenger count: {passengers.count()}")

        return render(request, 'airline_app/booking_success.html', {"booking": booking, "passengers": passengers})

    except Booking.DoesNotExist:
        print("Booking does not exist.")
        messages.error(request, "Booking not found.")
        return redirect("search_flights")

    except Exception as e:
        # Debugging: Log unexpected errors
        print("Unexpected error in booking_success:", str(e))
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect("search_flights")
    




@login_required
def view_bookings(request):
    # Adjust the related name based on your models
    bookings = Booking.objects.filter(customer=request.user).select_related('flight').prefetch_related('passengers')
    return render(request, 'airline_app/view_booking.html', {'bookings': bookings})



def edit_flights(request):
    """
    Displays all flights with edit buttons.
    """
    flights = Flight.objects.all()
    return render(request, 'airline_app/edit_flight.html', {'flights': flights})

def edit_flight_detail(request, flight_id):
    """
    Allows editing of a single flight.
    """
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == "POST":
        # Fetch updated data
        flight.origin = request.POST.get('origin')
        flight.destination = request.POST.get('destination')
        flight.departure_time = request.POST.get('departure_time')
        flight.arrival_time = request.POST.get('arrival_time')
        flight.available_seats = int(request.POST.get('available_seats'))
        flight.fare = float(request.POST.get('fare'))

        try:
            # Save the updated flight details
            flight.departure_time = timezone.datetime.fromisoformat(flight.departure_time)
            flight.arrival_time = timezone.datetime.fromisoformat(flight.arrival_time)
            flight.save()

            messages.success(request, "Flight updated successfully!")
            return redirect('edit_flights')

        except Exception as e:
            messages.error(request, f"Error updating flight: {e}")

    return render(request, 'airline_app/edit_flight_detail.html', {'flight': flight})




def delete_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    flight.delete()
    return redirect('delete_flights')  # Redirect to the general delete flights page

def delete_flights(request):
    flights = Flight.objects.all()
    return render(request, 'airline_app/delete_flight.html', {'flights': flights})


def view_flights(request):
    flights = Flight.objects.all()  # Fetch all flights from the database
    return render(request, 'airline_app/view_flights.html', {'flights': flights})





def view_customers(request):
    User = get_user_model()  # Get the custom User model
    customers = User.objects.all()  # Fetch all users from the database
    return render(request, 'airline_app/view_customers.html', {'customers': customers})



def admin_view_flights(request):
    # Fetch all flights from the database
    flights = Flight.objects.all()
    return render(request, 'airline_app/admin_view_flights.html', {'flights': flights})






def admin_view_passengers(request, flight_id):
    # Fetch the flight based on flight_id
    flight = get_object_or_404(Flight, id=flight_id)
    
    # Fetch passengers associated with the flight
    passengers = Passenger.objects.filter(booking__flight=flight)
    
    return render(request, 'airline_app/admin_view_passengers.html', {'flight': flight, 'passengers': passengers})


