from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from elections.controllers import get_user_from_email, create_user_from_data
from elections.serializers import LoginUserInputSerializer, VoterSerializer, MessageSerializer, UserIDSerializer, \
    VoterRegistrationSerializer


class RegisterUserAPI(APIView):
    """
    This is a view to use user registration and login
    """

    permission_classes = []

    @extend_schema(
        request=LoginUserInputSerializer,
        responses={
            200: VoterSerializer,
            401: ValidationError
        }
    )
    def get(self, request):
        request_data = LoginUserInputSerializer(data=request.data)
        request_data.is_valid(raise_exception=True)
        user = get_user_from_email(**request_data.validated_data)
        return Response(
            VoterSerializer(user).data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=VoterRegistrationSerializer,
        responses={
            200: UserIDSerializer,
            401: ValidationError
        }
    )
    def post(self, request):
        voter_data = VoterSerializer(data=request.data)
        voter_data.is_valid(raise_exception=True)
        user_id = create_user_from_data(**voter_data.validated_data)
        return Response(
            data=UserIDSerializer(data={
                'user_id': user_id
            }).data,
            status=status.HTTP_200_OK,
        )
