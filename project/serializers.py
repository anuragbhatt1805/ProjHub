from rest_framework import serializers
from project.models import Project, ProjectFile

from user.serializers import UserSerializer
from user.models import User

from fabricator.serializers import FabricatorSerializer
from fabricator.models import Fabricator

from team.serializers import TeamDetailSerializer
from team.models import Team

class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = '__all__'
        read_only_fields = ['id', 'project']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['manager'] = UserSerializer(User.objects.get(pk=response['manager'])).data
        response['fabricator'] = FabricatorSerializer(Fabricator.objects.get(pk=response['fabricator'])).data
        response['fabricator'].pop('contract')
        if response['team']:
            team = Team.objects.get(pk=response['team'])
            response['leader'] = UserSerializer(team.leader).data
        return response

class ProjectDetailSerializer(ProjectSerializer):

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields

    def to_representation(self, instance):
        request = self.context.get('request')
        response = super().to_representation(instance)
        response['manager'] = UserSerializer(User.objects.get(pk=response['manager'])).data
        response['fabricator'] = FabricatorSerializer(Fabricator.objects.get(pk=response['fabricator'])).data
        if request:
            response['fabricator']['contract'] = request.build_absolute_uri(response['fabricator']['contract'])
        response['team'] = TeamDetailSerializer(Team.objects.get(pk=response['team'])).data
        return response