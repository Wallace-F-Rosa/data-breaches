from rest_framework import serializers
from .models import *

class DataBreachSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBreach

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity

class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationType
