from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.views import ProjectViewSet, ProjectFileViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'project-files', ProjectFileViewSet, basename='projectfile')

urlpatterns = [
    path('', include(router.urls)),
]
