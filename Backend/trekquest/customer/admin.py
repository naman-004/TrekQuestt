from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Tour)
admin.site.register(Booking)
admin.site.register(Review)
# admin.site.register(UserManager)