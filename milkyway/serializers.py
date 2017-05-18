from django.contrib.auth.models import User, Group
from rest_framework import serializers
from milkyway.models import Assessment, Result, Iteration, Course

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups',)

class AssessmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assessment
        fields = ('start_date', 'description', 'end_date', 'iteration', 'title', 'id',)

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ('submitted', 'assessment', 'id', 'score', 'user',)

class IterationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Iteration
        fields = ('start_date', 'users', 'description', 'end_date', 'course', 'id',)

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'description', 'id',)
