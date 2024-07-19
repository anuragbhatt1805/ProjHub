from rest_framework import serializers
from fabricator.models import Fabricator

from datetime import datetime
import os

class FabricatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricator
        fields = '__all__'

class CSVFileSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def create(self, validated_data):
        csv_file = validated_data['csv_file']
        file_name = f"temp_user_{datetime.now()}.csv"
        current_directory = os.getcwd()
        file_directory = os.path.join(current_directory, 'static', 'temp')
        os.makedirs(file_directory, exist_ok=True)
        file_path = os.path.join(file_directory, file_name.replace(':', '_'))
        
        with open(file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        return file_path