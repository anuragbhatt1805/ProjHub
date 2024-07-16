from rest_framework import serializers
from fabricator.models import Fabricator

class FabricatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricator
        fields = '__all__'