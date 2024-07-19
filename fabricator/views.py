from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from fabricator.models import Fabricator
from fabricator.permissions import UpdateFabricator
from fabricator.serializers import FabricatorSerializer, CSVFileSerializer
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.http import FileResponse
from rest_framework.decorators import action
import os, csv


class FabricatorModelViewSet(viewsets.ModelViewSet):
    serializer_class = FabricatorSerializer
    queryset = Fabricator.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (UpdateFabricator, IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'contactPerson', 'contactCountry', 'contactState', 'contactCity')

    def get_serializer_class(self):
        if self.action == 'add_csv' or self.action == 'get_sample_csv':
            return CSVFileSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def get_sample_csv(self, request, pk=None):
        file_path = os.path.join(os.getcwd(), 'static', 'temp', 'fabricator_sample.csv')
        return FileResponse(
            open(file_path, 'rb'),
            filename='Sample Fabricator CSV File.csv',
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
                        Fabricator.objects.create(
                            name=row['name'],
                            contactPerson=row['person'],
                            contactPhone=row['phone'],
                            contactCountry=row['country'],
                            contactState=row['state'],
                            contactCity=row['city'],
                            contract=None
                        )
                        pass
                return Response(status=status.HTTP_201_CREATED)
            except FileNotFoundError:
                return Response({'error': 'CSV file not found'}, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)