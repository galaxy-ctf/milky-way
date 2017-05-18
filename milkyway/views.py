from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from milkyway.serializers import UserSerializer, GroupSerializer, AssessmentSerializer, ResultSerializer, IterationSerializer, CourseSerializer
from milkyway.models import Assessment, Result, Iteration, Course

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class IterationViewSet(viewsets.ModelViewSet):
    queryset = Iteration.objects.all()
    serializer_class = IterationSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
