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
from user.models import TaskRecord, User
from django.db.models import Q
from user.serializers import TaskRecordDetailSerializer
from datetime import date as today


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = [SearchFilter]
    search_fields = ['task', 'data', 'user']

class AssignedListViewSet(viewsets.ModelViewSet):
    queryset = AssignedList.objects.all()
    serializer_class = AssignedListSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = [SearchFilter, ]
    search_fields = ['task', 'assigned_by', 'assigned_to', 'approved_by', 'approved', 'comment']
    filter_fields = ['approved']

    def get_queryset(self):
        queryset = super().get_queryset()
        approved = self.request.query_params.get('approved')
        if approved is not None:
            queryset = queryset.filter(approved=approved)
        return queryset
    
    @action(detail=True, methods=['get', 'post', 'put', 'patch', 'delete'])
    def confirm(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'detail': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        assign = self.get_object()
        if assign.approved:
            return Response({'detail': 'Already Confirmed'}, status=status.HTTP_400_BAD_REQUEST)
        comment = request.data.get('comment')
        assign.confirm(approved_by=request.user, comment=comment)
        record = TaskRecord.objects.filter(user=request.user, task=assign.task).first()
        if record:
            record.add_end_punch()
            record.save()
        res = AssignedListSerializer(assign).data
        return Response(res, status=status.HTTP_200_OK)  


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = [SearchFilter, ]
    search_fields = ['fabricator', 'project', 'status', 'priority', 'due_date', 'duration', 'user', 'parent', 'name', 'description', ]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'my_task':
            return TaskDetailSerializer
        elif self.action == 'add_comment':
            return CommentSerializer
        elif self.action == 'add_assignes':
            return AssignedListSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            project = self.request.query_params.get('project', None)
            if project:
                return super().get_queryset().filter(project__id=project)
            return super().get_queryset()
        # return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset().filter(user=self.request.user)
    
    @action(detail=True, methods=['get', 'post'])
    def accept(self, request, pk=None):
        task = self.get_object()
        exisiting_rec = TaskRecord.objects.filter(task=task, user=request.user)
        if exisiting_rec.exists():
            return Response({'detail': 'Task already accepted'}, status=status.HTTP_400_BAD_REQUEST)
        record = TaskRecord.objects.create(
            task=task,
            user=request.user
        )
        record.save()
        # record.start()
        task.status = "ON-HOLD"
        task.save()

        data = TaskRecordDetailSerializer(record).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def my_task(self, request, pk=None):
        user = request.user
        info = Task.objects.filter(
            user=user,
            status__in=['IN-PROGRESS', 'BREAK']
        ).order_by('-priority', 'created_on').first()
        if info:
            serializer = self.get_serializer(info)
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        else:
            return Response({'detail': 'No tasks found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def my_task_list(self, request, pk=None):
        user = request.user
        info = Task.objects.filter(
            user=user,
            status__in=['ASSINGED', 'IN-PROGRESS', 'BREAK', 'ON-HOLD']
        ).order_by('-priority', 'created_on')
        
        serializer = self.get_serializer(info, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
        
    @action(detail=True, methods=['get', 'post'])
    def add_comment(self, request, pk=None):
        task = self.get_object()
        data = request.data.get('data')
        if not data:
            return Response({'detail': 'Data field is required'}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES.get('file')

        comment = task.add_comment(
            user=request.user,
            data=data,
            file=file
        )

        res = CommentSerializer(comment).data
        return Response(res, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get', 'post'])
    def add_assignes(self, request, pk=None ):
        task = self.get_object()
        assigned_by = request.user
        assigned_to = request.data.get('assigned_to')

        if not assigned_to:
            return Response({'detail':'Assigned To field is required'}, status=status.HTTP_400_BAD_REQUEST)

        comment = request.data.get('comment', "")

        assignList = task.add_assignes(
            assigned_by = assigned_by,
            assigned_to = User.objects.get(pk=assigned_to),
            comment = comment
        )

        res = AssignedListSerializer(assignList).data
        return Response(res, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get', ])
    def calender(self, request, pk=None):
        queryset = self.get_queryset()
        date = request.query_params.get('date', today.today())
        user = request.query_params.get('user', None)
        if not user:
            user = request.user
        else:
            user = User.objects.filter(
                Q(username=user) | Q(name__icontains=user) | Q(username=f'WBT-{user}') | Q(username=f'wbt-{user}')
            ).first()
        queryset = queryset.filter(user=user, created_on__lte=date,
                    status__in=['ASSINGED', 'IN-PROGRESS', 'BREAK', 'ON-HOLD'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)