from rest_framework import serializers
from user.models import (
    User, PushRecord, TaskRecord
)
from task.models import Task
from task.serializers import TaskSerializer
from rest_framework.parsers import FileUploadParser
import os
from datetime import datetime

class CSVFileSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def create(self, validated_data):
        csv_file = validated_data['csv_file']
        file_name = f"temp_user_{datetime.now()}.csv"
        current_directory = os.getcwd()
        file_directory = os.path.join(current_directory, 'static', 'temp')
        os.makedirs(file_directory, exist_ok=True)
        file_path = os.path.join(file_directory, file_name.replace(':', '_'))
        
        with open(file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        return file_path

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name',
            'is_active', 'is_staff', 'is_superuser',
            'password'
        ]
        extra_kwargs = {
            'password' : {
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    

class PunchRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushRecord
        fields = '__all__'
        read_only_fields = ['id', 'record', 'timestamp']

class TaskRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRecord
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.id
        return super().create(validated_data)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['task'] = TaskSerializer(Task.objects.get(pk=response['task'])).data
        response['user'] = UserSerializer(User.objects.get(pk=response['user'])).data
        response['time taken'] = instance.get_total_time()
        return response

class TaskRecordDetailSerializer(TaskRecordSerializer):
    class Meta:
        model = TaskRecord
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.id
        return super().create(validated_data)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['task'] = TaskSerializer(Task.objects.get(pk=response['task']['id'])).data
        response['user'] = UserSerializer(response['user']).data
        response['time_taken'] = instance.get_total_time()
        response['punches'] = PunchRecordSerializer(instance.get_punches(), many=True).data
        return response