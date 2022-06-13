from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from elections.api_helpers import user_dependent_call, user_election_dependent_call
from elections.controllers import get_user_from_email, create_user_from_data, get_elections_by_voter, \
    vote_for_candidate, get_election_details_by_user
from elections.models import Voter, Location
from elections.serializers import LoginUserInputSerializer, VoterSerializer, MessageSerializer, UserIDSerializer, \
    VoterRegistrationSerializer, ElectionSerializer, RetrieveElectionsSerializer, LocationSerializer, \
    VoteInputSerializer, CandidatesSerializer, \
    StatisticSerializer


class RegisterUserAPI(APIView):
    """
    This is a view to use user registration and login
    """

    permission_classes = []

    @extend_schema(
        request=VoterRegistrationSerializer,
        responses={
            200: UserIDSerializer,
            401: ValidationError
        }
    )
    def post(self, request):
        voter_data = VoterRegistrationSerializer(data=request.data)
        voter_data.is_valid(raise_exception=True)
        user_id = create_user_from_data(**voter_data.validated_data)

        user_id_data = UserIDSerializer(data={
            'user_id': user_id
        })
        user_id_data.is_valid(raise_exception=True)
        return Response(
            data=user_id_data.validated_data,
            status=status.HTTP_200_OK,
        )


class LoginUserAPI(APIView):
    """
    User login view
    """

    permission_classes = []

    @extend_schema(
        request=LoginUserInputSerializer,
        responses={
            200: VoterSerializer,
            401: ValidationError
        }
    )
    def post(self, request):
        request_data = LoginUserInputSerializer(data=request.data)
        request_data.is_valid(raise_exception=True)
        user = get_user_from_email(**request_data.validated_data)
        return Response(
            VoterSerializer(user).data,
            status=status.HTTP_200_OK
        )


class RetrieveElectionsAPI(APIView):
    """
    This is a view to get elections
    """

    permission_classes = []

    @extend_schema(
        request=RetrieveElectionsSerializer,
        responses={
            200: ElectionSerializer,
            401: ValidationError
        }
    )
    @user_dependent_call
    def get(self, request, voter: Voter):
        elections = get_elections_by_voter(voter)
        return Response(
            [ElectionSerializer.to_representation(election).data for election in elections],
            status=status.HTTP_200_OK
        )


class LocationsAPI(APIView):
    @extend_schema(
        responses={
            200: LocationSerializer,
            401: ValidationError
        }
    )
    def get(self, request):
        locations = Location.objects.all().order_by('city')
        return Response(
            LocationSerializer(locations, many=True).data,
            status=status.HTTP_200_OK
        )


class StatisticAPI(APIView):
    @extend_schema(
        responses={
            200: LocationSerializer,
            401: ValidationError
        }
    )
    @user_dependent_call
    def get(self, request, voter: Voter):
        elections = get_elections_by_voter(voter)
        return Response(
            StatisticSerializer(elections, many=True).data,
            status=status.HTTP_200_OK
        )


class VotingAPI(APIView):
    permission_classes = []

    @extend_schema(
        request=VoteInputSerializer,
        responses={
            200: {},
            400: ValidationError
        }
    )
    @user_dependent_call
    def post(self, request, voter: Voter):
        voting_data = VoteInputSerializer(data=request.data)
        voting_data.is_valid(raise_exception=True)
        vote_for_candidate(voter, **voting_data.validated_data)
        return Response(data={}, status=status.HTTP_200_OK)


class ElectionsAPI(APIView):
    permission_classes = []

    @extend_schema(
        responses={
            200: CandidatesSerializer
        }
    )
    @user_dependent_call
    def get(self, request, voter: Voter, election_id: int):
        election_candidate = get_election_details_by_user(election_id, voter)
        return Response(
            data={} if not election_candidate
            else CandidatesSerializer(
                election_candidate
            ).data,
            status=status.HTTP_202_ACCEPTED
        )

