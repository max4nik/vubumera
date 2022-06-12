from django.contrib import admin

# Register your models here.
from .models import Election, LocalElection, Candidate, Location

admin.site.register(Election)
admin.site.register(LocalElection)
admin.site.register(Candidate)
admin.site.register(Location)
