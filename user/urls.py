from rest_framework.routers import DefaultRouter
from django.urls import include, path
from user.views import (
    UserLoginApiView, UserModelViewSet
)


router = DefaultRouter()
router.register('emp', UserModelViewSet)

urlpatterns = [
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('', include(router.urls))
]
