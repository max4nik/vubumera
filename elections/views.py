from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from elections.api_helpers import user_dependent_call, user_election_dependent_call, election_dependent_call
from elections.controllers import VoterController, ElectionController
from elections.models import Voter, Location, Election
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
        controller = VoterController()
        user_id = controller.create_user_from_data(**voter_data.validated_data)

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
        controller = VoterController()
        user = controller.get_user_from_email(**request_data.validated_data)
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
        controller = VoterController(voter)
        elections = controller.get_elections_by_voter()
        return Response(
            [ElectionSerializer.to_representation(election).data for election in elections],
            status=status.HTTP_200_OK
        )


class GetElection(APIView):
    """
    This is a view to get election by id
    """

    permission_classes = []

    @extend_schema(
        request=RetrieveElectionsSerializer,
        responses={
            200: ElectionSerializer,
            401: ValidationError
        }
    )
    @election_dependent_call
    def get(self, request, election: Election):
        return Response(
            ElectionSerializer.to_representation(election).data,
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
        controller = VoterController()
        elections = controller.get_elections_by_voter()
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
        controller = VoterController(voter)
        controller.vote_for_candidate(**voting_data.validated_data)
        return Response(data={}, status=status.HTTP_200_OK)


class UnvoteAPI(APIView):
    permission_classes = []

    @extend_schema(
        responses={
            204: {},
            400: ValidationError
        }
    )
    @user_election_dependent_call
    def delete(self, request, voter: Voter, election: Election):
        controller = VoterController(voter)
        controller.unvote_in_election(election)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ElectionsAPI(APIView):
    permission_classes = []

    @extend_schema(
        responses={
            200: CandidatesSerializer
        }
    )
    @user_dependent_call
    def get(self, request, voter: Voter, election_id: int):
        controller = VoterController(voter)
        election_candidate = controller.get_election_details_by_user(election_id)
        return Response(
            data={} if not election_candidate
            else CandidatesSerializer(
                election_candidate
            ).data,
            status=status.HTTP_202_ACCEPTED
        )
