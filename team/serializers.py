from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from team.models import Team, Member


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
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

class MemberSerializer(ModelSerializer):

    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['id', 'team']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['employee'] = UserSerializer(get_user_model().objects.get(pk=response['employee'])).data
        return response

class TeamSerializer(ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['created_by'] = UserSerializer(get_user_model().objects.get(pk=response['created_by'])).data
        response['leader'] = UserSerializer(get_user_model().objects.get(pk=response['leader'])).data
        return response

class TeamDetailSerializer(ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['members'] = MemberSerializer(Member.objects.filter(team=instance), many=True).data
        response['created_by'] = UserSerializer(get_user_model().objects.get(pk=response['created_by'])).data
        response['leader'] = UserSerializer(get_user_model().objects.get(pk=response['leader'])).data
        return response
