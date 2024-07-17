from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.authentication import TokenAuthentication
from task.models import (
    TaskComment, Task, AssignedList
)
from task.serializers import (
    CommentSerializer, AssignedListSerializer,
    TaskSerializer, TaskDetailSerializer
)


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = [SearchFilter]
    search_fields = ['task', 'data', 'user']

class AssignedListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssignedList.objects.all()
    serializer_class = AssignedListSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = [SearchFilter, ]
    search_fields = ['task', 'assigned_by', 'assigned_to', 'approved_by', 'approved', 'comment']

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = [SearchFilter, ]
    search_fields = ['fabricator', 'project', 'status', 'priority', 'due_date', 'duration', 'user', 'parent', 'name', 'description', ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return super().get_serializer_class()