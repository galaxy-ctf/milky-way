from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from milkyway.serializers import UserSerializer, GroupSerializer, SolvesSerializer, FlagSerializer, ChallengeSerializer
from milkyway.models import Solves, Flag, Challenge

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SolvesViewSet(viewsets.ModelViewSet):
    queryset = Solves.objects.all()
    serializer_class = SolvesSerializer

class FlagViewSet(viewsets.ModelViewSet):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
