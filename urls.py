from django.urls import path
from . import views

urlpatterns = [
    # Define URLs for the app here
    path('home', views.home, name='home'),  # Example for the homepage
    path('register/',views.register_user, name='register'),
    path('customer_dashboard/',views.customer_dashboard, name='customer_dashboard'),
    path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('login/',views.user_login, name='login'),
    path('customer_booking',views.customer_booking, name='customer_booking'),
    path('add_flight',views.adding_flight, name='add_flight'),
    path('search-flights/', views.search_flights, name='search_flights'),
    path('book-flight/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('view-bookings/', views.view_bookings, name='view-bookings'),
    path('edit-flights/', views.edit_flights, name='edit_flights'),
    path('edit-flight/<int:flight_id>/', views.edit_flight_detail, name='edit_flight_detail'),
    path('delete-flight/<int:flight_id>/', views.delete_flight, name='delete_flight'),
    path('delete-flights/', views.delete_flights, name='delete_flights'),
    path('view-flights/', views.view_flights, name='view_flights'),
    path('view-customers/', views.view_customers, name='view_customers'),
    path('admin_flights/', views.admin_view_flights, name='admin_view_flights'),
    path('admin_flights/<int:flight_id>/passengers/', views.admin_view_passengers, name='admin_view_passengers'),
]
    




