from typing import Optional
from itertools import chain
from rest_framework.exceptions import ValidationError

from elections.models import Voter, Election, LocalElection, Location


def get_elections_by_voter(voter: Voter):
    local_elections_for_voter: LocalElection = LocalElection.objects.filter(location=voter.location)
    global_elections: Election = Election.objects.all()
    all_elections = local_elections_for_voter | global_elections


def get_user_from_email(email: str, password: str) -> Optional[Voter]:
    suspect: Voter = Voter.objects.get(email=email).first()
    if suspect.check_password(password):
       return suspect
    else:
        raise ValidationError(detail='Password is incorrect', code=401)


def create_user_from_data(password: str, **kwargs):
    location_data = kwargs['location']
    location = Location.objects.get_or_create(**location_data).first()
    location.save()
    new_voter = Voter(location=location, **kwargs)
    new_voter.set_password(password)
    new_voter.save()
    return new_voter.id
