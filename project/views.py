from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.authentication import TokenAuthentication
from project.models import Project, ProjectFile
from project.serializers import (
    ProjectSerializer, ProjectFileSerializer,
    ProjectDetailSerializer
) 
from project.permissions import IsSuperuserOrReadOnly
from team.models import Team, Member

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsSuperuserOrReadOnly, ]
    filter_backends = [SearchFilter, ]
    search_fields = ['name', 'description', 'manager', 'team', 'fabricator', 'status', 'stage']

    def get_serializer_class(self):
        if self.action == 'add_file':
            return ProjectFileSerializer
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return super().get_queryset()
        else:
            members = Member.objects.filter(employee=self.request.user)
            team_ids = set([member.team for member in members])
            projects = Project.objects.filter(team__in=team_ids)
            if projects.count() > 0:
                return projects
            return []

    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        project = self.get_object()
        files = project.get_all_files()
        serializer = ProjectFileSerializer(files, many=True)
        updated_files = []
        for file in serializer.data:
            file['file'] = request.build_absolute_uri(file['file'])
            updated_files.append(file)
        return Response(updated_files)

    @action(detail=True, methods=['post', 'get'],)
    def add_file(self, request, pk=None):
        project = self.get_object()
        file = request.FILES.get('file')
        detail = request.data.get('detail')
        
        if not file:
            return Response({"detail": "File is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProjectFileSerializer(data={'file': file, 'detail': detail})
        if serializer.is_valid():
            project.add_file(file, detail)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectFileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectFile.objects.all()
    authentication_classes = [TokenAuthentication, ]
    serializer_class = ProjectFileSerializer
    permission_classes = [IsAuthenticated, IsSuperuserOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project__id=project_id)
        return queryset
