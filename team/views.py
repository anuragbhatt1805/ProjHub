from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from team.permissions import IsSuperuserOrReadOnly
from team.models import Team, Member
from user.models import User
from team.serializers import MemberSerializer, TeamSerializer, TeamDetailSerializer

class TeamMemberViewSet(ReadOnlyModelViewSet):
    queryset = Member.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsSuperuserOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        team_id = self.request.query_params.get('team_id')
        if team_id:
            queryset = queryset.filter(team__id=team_id)
        return queryset
    
class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuserOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamSerializer
        if self.action == 'retrieve':
            return TeamDetailSerializer
        if self.action == 'members' or self.action == 'add_member':
            return MemberSerializer
        return super().get_serializer_class()
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        team = self.get_object()
        members = team.get_members()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get', 'post'])
    def add_member(self, request, pk=None):
        team = self.get_object()
        employee = request.data.get('employee')
        role = request.data.get('role')
        serializer = MemberSerializer(data={
            'employee': employee,
            'role': role
        })
        if serializer.is_valid():
            team.add_member(role, User.objects.get(pk=employee))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='remove_member/(?P<member_id>[^/.]+)')
    def remove_member(self, request, pk=None, member_id=None):
        team = self.get_object()
        member = team.remove_member(member_id)
        if not member:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'], url_path='member_role/(?P<member_id>[^/.]+)')
    def member_role(self, request, pk=None, member_id=None):
        team = self.get_object()
        role = team.get_member_role(member_id)
        if not role:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(role)
