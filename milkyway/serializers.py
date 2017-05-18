from django.contrib.auth.models import User, Group
from rest_framework import serializers
from milkyway.models import Solves, Flag, Challenge

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups',)

class SolvesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Solves
        fields = ('id', 'challenge', 'team',)

class FlagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Flag
        fields = ('id', 'flag_is_regex', 'flags', 'chal',)

class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Challenge
        fields = ('category', 'name', 'value', 'id', 'description', 'hidden',)
