from functools import wraps

from rest_framework import status, request
from rest_framework.response import Response

from elections.models import Voter, Election


def user_dependent_call(func):

    @wraps(func)
    def __wrapped__(*args, **kwargs):
        try:
            user_id = kwargs['user_id']
            user = Voter.objects.get(id=user_id)
            kwargs.pop('user_id')
        except KeyError:
            return Response(
                data={
                    'message': 'No user id provided'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        response = func(*args, voter=user, **kwargs)
        return response

    return __wrapped__


def user_election_dependent_call(func):

    @wraps(func)
    def __wrapped__(*args, **kwargs):
        try:
            user_id = kwargs['user_id']
            user = Voter.objects.get(id=user_id)
            election_id = kwargs['election_id']
            election = Election.objects.get(id=election_id)
        except KeyError:
            return Response(
                data={
                    'message': 'Bad data provided'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        response = func(*args, voter=user, election=election)
        return response

    return __wrapped__