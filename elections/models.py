import json

from django.contrib.auth.models import User
from django.core import serializers
from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.city}'


class Voter(User):
    full_name = models.CharField(max_length=64)
    passport_id = models.CharField(max_length=32)
    birthdate = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Election(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    is_flexible = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def candidates(self):
        return Candidate.objects.filter(election=self)


class GlobalElection(Election):
    pass


class LocalElection(Election):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class Candidate(models.Model):
    full_name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.full_name


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
