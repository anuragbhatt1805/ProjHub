from rest_framework.routers import DefaultRouter
from django.urls import include, path
from user.views import (
    UserLoginApiView, UserModelViewSet,
    PunchRecordViewSet,
    TaskRecordViewSet
)


router = DefaultRouter()
router.register('emp', UserModelViewSet)
router.register('punch', PunchRecordViewSet)
router.register('record', TaskRecordViewSet)

urlpatterns = [
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('', include(router.urls))
]
