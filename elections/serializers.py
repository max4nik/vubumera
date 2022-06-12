from rest_framework import serializers

from elections.models import Voter, Election, Location, LocalElection


class LoginUserInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=145)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        exclude = 'id'


class VoterSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)

    class Meta:
        model = Voter
        fields = [
            'id', 'full_name', 'email', 'password_id', 'birthdate', 'location'
        ]


class VoterRegistrationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)

    class Meta:
        model = Voter
        fields = [
            'id', 'full_name', 'email', 'password_id', 'birthdate', 'password', 'location'
        ]


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'


class LocalElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalElection
        fields = '__all__'


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=250)


class UserIDSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
