from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task.views import (
    CommentViewSet, AssignedListViewSet,
    TaskViewSet
)

router = DefaultRouter()
router.register('comments', CommentViewSet)
router.register('assigned-list', AssignedListViewSet)
router.register('tasks', TaskViewSet)


urlpatterns = [
    path('', include(router.urls)),
]