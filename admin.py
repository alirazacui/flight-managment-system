from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(Report)
admin.site.register(Passenger)
