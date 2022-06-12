from typing import List

from rest_framework import serializers

from elections.models import Voter, Election, Location, LocalElection, GlobalElection, Candidate
from elections.services import get_candidate_votes_for_election


class LoginUserInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=145)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['region', 'city']


class RetrieveElectionsSerializer(serializers.Serializer):

    class Meta:
        model = Location
        fields = '__all__'


class CandidatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class VoterSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)

    class Meta:
        model = Voter
        fields = [
            'id', 'full_name', 'email', 'passport_id', 'birthdate', 'location'
        ]


class VoterRegistrationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)

    class Meta:
        model = Voter
        fields = [
            'id', 'full_name', 'email', 'passport_id', 'birthdate', 'password', 'location'
        ]


class ElectionSerializer(serializers.ModelSerializer):
    @classmethod
    def to_representation(cls, instance):
        if isinstance(instance, LocalElection):
            return LocalElectionSerializer(instance=instance)
        elif isinstance(instance, GlobalElection):
            return GlobalElectionSerializer(instance=instance)

    class Meta:
        model = Election
        fields = '__all__'


class GlobalElectionSerializer(serializers.ModelSerializer):
    candidates = CandidatesSerializer(many=True)

    class Meta:
        model = GlobalElection
        fields = ['id', 'name', 'description', 'is_flexible', 'start_date', 'end_date', 'candidates']


class LocalElectionSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)
    candidates = CandidatesSerializer(many=True)

    class Meta:
        model = LocalElection
        fields = ['id', 'name', 'description', 'is_flexible', 'start_date', 'end_date', 'location', 'candidates']


class MessageSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=250)


class UserIDSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class VoteInputSerializer(serializers.Serializer):
    election_id = serializers.IntegerField()
    candidate_id = serializers.IntegerField()


class VotingResultSerializer(serializers.Serializer):
    candidate: CandidatesSerializer(many=False)
    vote_count: serializers.IntegerField()


class ElectionFullSerializer(serializers.ModelSerializer):
    vote_results = VotingResultSerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = '__all__'


class ElectionFullSerializerImplementation(serializers.ModelSerializer):
    vote_results = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = '__all__'

    def get_candidate_votes(self, obj) -> List[VotingResultSerializer]:
        candidate_votes = get_candidate_votes_for_election(obj)
        return [VotingResultSerializer(vote) for vote in candidate_votes]
