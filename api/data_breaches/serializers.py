from rest_framework import serializers
from django.db import transaction
from .models import *

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class EntitySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
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

    def to_representation(self, obj):
        """
        Override to return correct representation of the DataBreach object as a
        dictionary with nested Entity, OrganizationType and Source objects.

        Args:
            obj (DataBreach) : The DataBreach object.

        Returns:
            Dictionary with correct DataBreach data representantion.
        Example of correct representation:

        .. code-block:: json

            {
                "id" : 1,
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
        entity = Entity.objects.get(pk=obj.entity.id)
        org_type = OrganizationType.objects.filter(entity=entity)
        sources = Source.objects.filter(data_breach=obj)
        
        return {
            'id' : obj.id,
            'entity' : {
                'name' : entity.name,
                'organization_type' : [org.organization_type for org in org_type]
            },
            'year' : obj.year,
            'records' : obj.records,
            'method' : obj.method,
            'sources' : [s.url for s in sources]
        }

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

            # create organization type
            entity, created = Entity.objects.get_or_create(name=entity_data['name'])
            if created:
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
                org_serializer.save()

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
            source_serializer.save()
        return databreach
