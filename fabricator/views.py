from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from fabricator.models import Fabricator
from fabricator.permissions import UpdateFabricator
from fabricator.serializers import FabricatorSerializer


class FabricatorModelViewSet(viewsets.ModelViewSet):
    serializer_class = FabricatorSerializer
    queryset = Fabricator.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (UpdateFabricator, IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'contactPerson', 'contactCountry', 'contactState', 'contactCity')