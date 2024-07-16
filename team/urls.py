from django.urls import path, include
from rest_framework.routers import DefaultRouter
from team.views import TeamViewSet, TeamMemberViewSet


router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'members', TeamMemberViewSet, basename='teamMembers')

urlpatterns = [
    path('', include(router.urls)),
]
