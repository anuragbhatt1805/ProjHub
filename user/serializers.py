from rest_framework import serializers
from user.models import (
    User, PushRecord, TaskRecord
)
from task.models import Task

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
        read_only_fields = ['id', 'record']

class TaskRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRecord
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.id
        return super().create(validated_data)
    
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['task'] = TaskSerializer(Task.objects.get(pk=response['task'])).data
    #     response['user'] = UserSerializer(User.objects.get(pk=response['user'])).data
    #     response['time taken'] = instance.get_total_time()
    #     return response

class TaskRecordDetailSerializer(TaskRecordSerializer):
    class Meta:
        model = TaskRecord
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.id
        return super().create(validated_data)
    
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['task'] = TaskSerializer(Task.objects.get(pk=response['task'])).data
    #     response['user'] = UserSerializer(User.objects.get(pk=response['user'])).data
    #     response['time taken'] = instance.get_total_time()
    #     response['punches'] = PunchRecordSerializer(instance.get_punches(), many=True).data
    #     return response