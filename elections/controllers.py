from typing import Optional, List
from itertools import chain

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from elections.models import Voter, GlobalElection, LocalElection, Location, Vote, Election, Candidate

def get_elections_by_voter(voter: Voter):
    local_elections_for_voter: LocalElection = LocalElection.objects.filter(location=voter.location)
    global_elections: GlobalElection = GlobalElection.objects.all()
    return chain(global_elections, local_elections_for_voter)


def get_user_from_email(email: str, password: str) -> Optional[Voter]:
    suspect: Voter = Voter.objects.filter(email=email).first()
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
    try:
        previous_vote = Vote.objects.get(voter_id=voter.id, election_id=election_id)
    except Vote.DoesNotExist:
        previous_vote = None
    election: Election = Election.objects.get(id=election_id)
    candidate: Candidate = Candidate.objects.get(id=candidate_id)
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
    try:
        previous_vote = Vote.objects.get(voter_id=voter.id, election_id=election_id)
    except Vote.DoesNotExist:
        previous_vote = None
    candidate = None
    if previous_vote:
        candidate = Candidate.objects.get(id=previous_vote.candidate_id)
    return candidate


def get_percents_by_candidate_for_election(election: Election):
    candidates = election.candidates
    result = [[], []]
    for candidate in candidates:
        result[0].append(candidate.full_name)
        result[1].append(0)
    votes = Vote.objects.filter(election=election)
    candidates = votes.values_list('candidate')
    candidates_count = len(candidates)
    candidates = set(candidates)

    for candidate in candidates:
        votes_by_candidates = Vote.objects.filter(candidate_id=candidate[0])
        candidate = votes_by_candidates.first().candidate
        candidate_counter = votes_by_candidates.count()
        index_for_second_list = result[0].index(candidate.full_name)
        result[1][index_for_second_list] = candidate_counter / candidates_count * 100
    return result
