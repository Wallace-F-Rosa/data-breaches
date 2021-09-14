from rest_framework import serializers
from django.db import transaction
from .models import *

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'

class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationType
        fields = '__all__'

class DataBreachSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBreach
        fields = '__all__'

    entity = EntitySerializer()

    def create(self, validated_data):
        """
        Override to create Entity, OrganizationType and Source objects
        using context to pass extra data to serializer. All objects are
        created in a transaction so either the operation is successfull 
        or a rollback will be called.

        Extra data:
            * entity (dict) : entity data is passed as the organization `name` and a list of str with words describing the sphere of action of the organization, `organization_type`.

            * sources (list) : list of urls of midia sources that described the data breach.

        Example :

        .. code-block:: json

            {
                "entity" : {
                    "name" : "Test",
                    "organization_type" : ["web"]
                },
                "year" : 2021,
                "records" : 10000,
                "method" : "hacking",
                "sources" : ["https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal"]
            }

        """
        databreach = None
        with transaction.atomic() :
            # create entity
            entity_data = validated_data.pop('entity')
            entity_serializer = EntitySerializer(data={
                'name' : entity_data['name']
            })
            if not entity_serializer.is_valid():
                raise serializers.ValidationError(entity_serializer.errors)
            entity = entity_serializer.save()

            # create organization type
            org_data = self.context['request'].data['entity']['organization_type']
            orgs = []
            for org in org_data:
                orgs.append({
                    'organization_type' : org,
                    'entity' : entity.id
                })
            org_serializer = OrganizationTypeSerializer(data=orgs, many=True)
            if not org_serializer.is_valid():
                raise serializers.ValidationError(org_serializer.errors)

            # create databreach object
            databreach = DataBreach.objects.create(**validated_data, entity=entity)

            # create sources
            source_data = self.context['request'].data['sources']
            sources = []
            for source in source_data:
                sources.append({
                    'url' : source,
                    'data_breach' : databreach.id
                })
            source_serializer = SourceSerializer(data=sources, many=True)
            if not source_serializer.is_valid():
                raise serializers.ValidationError(source_serializer.errors)

        return databreach
