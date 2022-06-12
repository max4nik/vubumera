from functools import wraps

from rest_framework import status, request
from rest_framework.response import Response

from elections.models import Voter


def user_dependent_call(func):

    @wraps(func)
    def __wrapped__(*args, **kwargs):
        try:
            user_id = kwargs['user_id']
            user = Voter.objects.get(id=user_id)
        except KeyError:
            return Response(
                data={
                    'message': 'No user id provided'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        response = func(*args, voter=user)
        return response

    return __wrapped__


