from rest_framework import serializers
from task.models import (
    TaskComment, Task, AssignedList
)

from django.contrib.auth import get_user_model
from user.models import TaskRecord

from project.models import Project
from project.serializers import ProjectDetailSerializer, ProjectSerializer, UserSerializer

from fabricator.models import Fabricator
from fabricator.serializers import FabricatorSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = '__all__'
        read_only_fields = ['id', 'task', 'created_on', 'user']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(get_user_model().objects.get(pk=response['user'])).data
        return response
    

class AssignedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedList
        fields = '__all__'
        read_only_fields = ['id', 'task', 'created_on', 'approved_on', 'assigned_on', 'assigned_by']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['task'] = TaskSerializer(Task.objects.get(pk=response['task'])).data
        response['assigned_by'] = UserSerializer(get_user_model().objects.get(pk=response['assigned_by'])).data
        response['assigned_to'] = UserSerializer(get_user_model().objects.get(pk=response['assigned_to'])).data
        if response['approved']:
            response['approved_by'] = UserSerializer(get_user_model().objects.get(pk=response['approved_by'])).data
        return response
    

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_on', 'updated_on', 'fabricator',]
    
    def to_representation(self, instance):
        request = self.context.get('request')
        response = super().to_representation(instance)
        response['fabricator'] = FabricatorSerializer(Fabricator.objects.get(pk=response['fabricator'])).data
        if request:
            response['fabricator']['contract'] = request.build_absolute_uri(response['fabricator']['contract'])
        response['project'] = ProjectSerializer(Project.objects.get(pk=response['project'])).data
        response['user'] = UserSerializer(get_user_model().objects.get(pk=response['user'])).data
        return response
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['assigned_by'] = request.user
        # print(validated_data)
        # validated_data['project'] = Project.objects.get(pk=validated_data['project'].id)
        # print(validated_data)
        return super().create(validated_data)

class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_on', 'updated_on', 'fabricator', 'project']
    
    def to_representation(self, instance):
        request = self.context.get('request')
        response = super().to_representation(instance)
        record = TaskRecord.objects.filter(user=request.user, task=instance)
        if record.exists():
            response['record'] = record.first().id
        response['fabricator'] = FabricatorSerializer(Fabricator.objects.get(pk=response['fabricator'])).data
        if request:
            response['fabricator']['contract'] = request.build_absolute_uri(response['fabricator']['contract'])
        response['project'] = ProjectDetailSerializer(Project.objects.get(pk=response['project'])).data
        response['user'] = UserSerializer(get_user_model().objects.get(pk=response['user'])).data
        if response['parent']:
            response['parent'] = TaskSerializer(Task.objects.get(pk=response['parent'])).data
        response['child'] = TaskSerializer(instance.get_child_tasks(), many=True).data
        comments = CommentSerializer(instance.get_comments(), many=True).data
        for comment in comments:
            if comment['file']:
                comment['file'] = request.build_absolute_uri(comment['file'])
        response['comments'] = comments
        response['assigned'] = AssignedListSerializer(instance.get_assignes(), many=True).data
        return response