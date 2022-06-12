from collections import defaultdict
from itertools import groupby
from typing import List, Tuple, Dict

from elections.models import Election, Vote, Candidate


def get_candidate_votes_for_election(election: Election) -> List[Dict[str, Candidate]]:
    try:
        votes = Vote.objects.filter(election_id=election.id)
    except Vote.DoesNotExist:
        votes = []
    voting_results = defaultdict(int)

    for vote in votes:
        voting_results[vote.candidate_id] += 1

    final_results = []
    for result in voting_results:
        final_results.append(
            dict(
                candidate=Candidate.objects.get(id=result),
                vote_count=voting_results[result]
            )
        )

    return final_results
