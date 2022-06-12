from functools import wraps

from rest_framework import status, request
from rest_framework.response import Response

from elections.models import Voter


def user_dependent_call(func):

    @wraps(func)
    def __wrapped__(*args, **kwargs):
        rq: request.Request = args[0]
        if 'user_id' in rq.data:
            user = Voter.objects.get(id=rq.data['user_id']).first()
        else:
            return Response(
                data={
                    'message': 'No user id provided'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        response = func(*args, voter=user, **kwargs)
        return response

    return __wrapped__


