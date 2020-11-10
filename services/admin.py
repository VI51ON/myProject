from django.contrib import admin
from .models import Service, Contact, Event
# Register your models here.

admin.site.register(Service)
admin.site.register(Contact)
admin.site.register(Event)