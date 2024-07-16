from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from user.models import (
    User, PushRecord, TaskRecord
)
from user.permissions import (
    UpdateOwnProfile
)
from user.serializers import (
    UserSerializer,
    PunchRecordSerializer,
    TaskRecordSerializer,
    TaskRecordDetailSerializer
)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user Authentication Token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (UpdateOwnProfile, IsAuthenticated)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'username', 'email', 'is_staff', 'is_superuser')


class PunchRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PunchRecordSerializer
    queryset = PushRecord.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

class TaskRecordViewSet(viewsets.ModelViewSet):
    serializer_class = TaskRecordSerializer
    queryset = TaskRecord.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('task', 'user')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskRecordDetailSerializer
        return super().get_serializer_class()
    
    @action(detail=True, methods=['get', 'post'])
    def start(self, request, pk=None):
        record = self.get_object()
        punch = record.add_start_punch()
        serializer = PunchRecordSerializer(punch)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'])
    def end(self, request, pk=None):
        record = self.get_object()
        punch = record.add_end_punch()
        serializer = PunchRecordSerializer(punch)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get', 'post'])
    def resume(self, request, pk=None):
        record = self.get_object()
        punch = record.add_resume_punch()
        serializer = PunchRecordSerializer(punch)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get', 'post'])
    def pause(self, request, pk=None):
        record = self.get_object()
        punch = record.add_suspend_record()
        serializer = PunchRecordSerializer(punch)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def punches(self, request, pk=None):
        record = self.get_object()
        punches = record.get_punches()
        serializer = PunchRecordSerializer(punches, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def time(self, request, pk=None):
        record = self.get_object()
        time = record.get_total_time()
        return Response({'time': time})