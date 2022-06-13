from collections import defaultdict
from itertools import groupby
from typing import List, Tuple, Dict

from elections.models import Election, Vote, Candidate


def get_candidate_votes_for_election(election: Election):
    try:
        votes = Vote.objects.filter(election_id=election.id)
    except Vote.DoesNotExist:
        votes = []
    voting_results = defaultdict(int)

    for vote in votes:
        voting_results[vote.candidate_id] += 1

    all_candidates = Candidate.objects.filter(election_id=election.id).all()

    for cand in all_candidates:
        if cand.id not in voting_results:
            voting_results[cand.id] = 0

    final_results = [[], []]
    for result in voting_results:
        final_results[0].append(
                Candidate.objects.get(id=result).full_name
            )
        final_results[1].append(voting_results[result])

    return final_results
