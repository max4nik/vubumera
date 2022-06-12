from collections import defaultdict
from itertools import groupby
from typing import List, Tuple, Dict

from elections.models import Election, Vote, Candidate


def get_candidate_votes_for_election(election: Election) -> List[Dict[str, Candidate, str, int]]:
    votes = Vote.objects.get(election_id=election.id).all()
    voting_results = []
    for key, group in groupby(votes, lambda x: x.candidate_id):
        voting_results.append(
            dict(
                candidate=Candidate.objects.get(id=key).first(),
                vote_count=len(group)
            )
        )
    return voting_results
