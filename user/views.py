from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from django.core.exceptions import ValidationError
import csv, os
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
    TaskRecordDetailSerializer,
    CSVFileSerializer
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

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(is_superuser=False)

    def get_serializer_class(self):
        if self.action == 'add_csv' or self.action == 'get_sample_csv':
            return CSVFileSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get', 'post', 'put', 'delete', 'patch'])
    def me(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user).data
        return Response(serializer, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_sample_csv(self, request, pk=None):
        file_path = os.path.join(os.getcwd(), 'static', 'temp', 'user_sample.csv')
        return FileResponse(
            open(file_path, 'rb'),
            filename='Sample User CSV File.csv',
            as_attachment=True,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['post', 'get'])
    def add_csv(self, request, pk=None):
        serializer = CSVFileSerializer(data=request.data)
        if serializer.is_valid():
            file_path = serializer.save()
            try:
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        User.objects.create(
                            username=row['username'], 
                            email=row['email'], 
                            name=row['name'],
                            password=row.get('password', 'Qwerty!2345678'),
                            is_superuser=True if row['role'].lower() == 'admin' else False,
                            is_staff=True if (row['role'].lower() == 'manager' or row['role'].lower() == 'admin') else False
                        )
                return Response(status=status.HTTP_201_CREATED)
            except FileNotFoundError:
                return Response({'error': 'CSV file not found'}, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get('user', None)
        if not user:
            user = self.request.user
        else:
            user = User.objects.filter(
                username__in=[user, f'WBT-{user}', f'wbt-{user}']
            ).first()
        queryset = queryset.filter(user=user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskRecordDetailSerializer
        if self.action in ['start', 'end', 'resume', 'pause', 'punches']:
            return PunchRecordSerializer
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