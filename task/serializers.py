from rest_framework import serializers
from task.models import (
    TaskComment, Task, AssignedList
)

from user.models import User
from user.serializers import UserSerializer

from project.models import Project
from project.serializers import ProjectDetailSerializer

from fabricator.models import Fabricator
from fabricator.serializers import FabricatorSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = '__all__'
        read_only_fields = ['id', 'task', 'created_on']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(User.objects.get(pk=response['user'])).data
        return response
    

class AssignedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedList
        fields = '__all__'
        read_only_fields = ['id', 'task', 'created_on', 'approved_on', 'assigned_on']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['assigned_by'] = UserSerializer(User.objects.get(pk=response['assigned_by'])).data
        response['assigned_to'] = UserSerializer(User.objects.get(pk=response['assigned_to'])).data
        response['approved_by'] = UserSerializer(User.objects.get(pk=response['approved_by'])).data
        return 
    

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_on', 'updated_on', 'fabricator', 'project']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['fabricator'] = FabricatorSerializer(Fabricator.objects.get(pk=response['fabricator'])).data
        response['project'] = ProjectDetailSerializer(Project.objects.get(pk=response['project'])).data
        response['user'] = UserSerializer(User.objects.get(pk=response['user'])).data
        return response

class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_on', 'updated_on', 'fabricator', 'project']
    
    def to_representation(self, instance):
        request = self.context.get('request')
        response = super().to_representation(instance)
        response['fabricator'] = FabricatorSerializer(Fabricator.objects.get(pk=response['fabricator'])).data
        response['project'] = ProjectDetailSerializer(Project.objects.get(pk=response['project'])).data
        response['user'] = UserSerializer(User.objects.get(pk=response['user'])).data
        if response['parent']:
            response['parent'] = TaskSerializer(Task.objects.get(pk=response['parent'])).data
        response['child'] = TaskSerializer(Task.objects.filter(parent=response['id']), many=True).data
        comments = CommentSerializer(TaskComment.objects.filter(task=response['id']), many=True).data
        for comment in comments:
            comment['file'] = request.build_absolute_uri(comment['file'])
        response['comments'] = comments
        response['assigned'] = AssignedListSerializer(AssignedList.objects.filter(task=response['id']), many=True).data
        return response