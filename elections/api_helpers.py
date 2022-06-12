from functools import wraps

from django.shortcuts import get_object_or_404
from rest_framework import status, request
from rest_framework.response import Response

from elections.models import Voter


def user_dependent_call(func):

    @wraps(func)
    def __wrapped__(*args, **kwargs):
        try:
            user_id = kwargs['user_id']
            user = get_object_or_404(Voter, id=user_id)
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


