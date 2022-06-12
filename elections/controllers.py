from typing import Optional, List
from itertools import chain
from rest_framework.exceptions import ValidationError

from elections.models import Voter, GlobalElection, LocalElection, Location, Vote, Election, Candidate
from elections.serializers import ElectionFullSerializerImplementation


def get_elections_by_voter(voter: Voter):
    local_elections_for_voter: LocalElection = LocalElection.objects.filter(location=voter.location)
    global_elections: GlobalElection = GlobalElection.objects.all()
    return chain(local_elections_for_voter, global_elections)


def get_user_from_email(email: str, password: str) -> Optional[Voter]:
    suspect: Voter = Voter.objects.get(email=email).first()
    if suspect.check_password(password):
        return suspect
    else:
        raise ValidationError(detail='Password is incorrect', code=401)


def create_user_from_data(password: str, **kwargs):
    location_data = kwargs['location']
    location = Location.objects.get(**location_data)
    kwargs['location'] = location
    kwargs['username'] = kwargs['passport_id']  # заглушка на username
    new_voter = Voter(**kwargs)
    new_voter.set_password(password)
    new_voter.save()
    return new_voter.id


def vote_for_candidate(voter: Voter, candidate_id: int, election_id: int):
    previous_vote: Vote = Vote.objects.get(voter_id=voter.id, election_id=election_id).first()
    election: Election = Election.objects.get(id=election_id).first()
    candidate: Candidate = Candidate.objects.get(id=candidate_id).first()
    if previous_vote and not election.is_flexible:
        raise ValidationError(detail='It is impossible to change a vote on this election', code=400)
    elif previous_vote:
        previous_vote.candidate = candidate
        previous_vote.save()
    else:
        new_vote = Vote(voter_id=voter.id, candidate_id=candidate_id, election_id=election_id)
        new_vote.save()
    return None


def get_election_details_by_user(election_id: int, voter: Voter) -> Optional[Candidate]:
    previous_vote: Vote = Vote.objects.get(voter_id=voter.id, election_id=election_id).first()
    candidate = None
    if previous_vote:
        candidate = Candidate.objects.get(id=previous_vote.candidate_id)
    return candidate


def get_election_detail_serializer_by_location(voter: Voter):
    elections = get_elections_by_voter(voter)
    return ElectionFullSerializerImplementation(elections, many=True)
