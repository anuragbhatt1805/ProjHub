from rest_framework.serializers import ModelSerializer
from user.models import User
from user.serializers import UserSerializer
from team.models import Team, Member

class MemberSerializer(ModelSerializer):

    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['id', 'team']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['employee'] = UserSerializer(User.objects.get(pk=response['employee'])).data
        return response

class TeamSerializer(ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['created_by'] = UserSerializer(User.objects.get(pk=response['created_by'])).data
        response['leader'] = UserSerializer(User.objects.get(pk=response['leader'])).data
        return response

class TeamDetailSerializer(ModelSerializer):

    class Meta:
        model = Team
        fields = ['id', 'created_by', 'leader', 'created_at', ]
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['members'] = MemberSerializer(Member.objects.filter(team=instance), many=True).data
        response['created_by'] = UserSerializer(User.objects.get(pk=response['created_by'])).data
        response['leader'] = UserSerializer(User.objects.get(pk=response['leader'])).data
        return response
