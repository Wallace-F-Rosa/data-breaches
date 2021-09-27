from rest_framework import serializers
from django.db import transaction
from .models import *

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationType
        fields = '__all__'

class EntitySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Entity
        fields = '__all__'

    def to_representation(self, obj):
        """Override to return correct representation of Entity object.
        Example:

        .. code-block:: json

            {
                "id" : 1,
                "name" : "Test",
                "organization_type" : ["web"]
            }
        """

        org_type = OrganizationType.objects.filter(entity=obj)

        return {
            'id': obj.id,
            'name': obj.name,
            'organization_type': [t.organization_type for t in org_type]
        }

    def create(self, validated_data):
        """Override to create Entity and OrganizationType objects with extra content
        passed in context.
        Extra data:
            * organization_type (list) : list of strings containing the organization sphere
        of action.
        """
        with transaction.atomic():
            entity, created = Entity.objects.get_or_create(name=validated_data['name'])
            if created:
                org_data = self.context['extra'].get('organization_type', [])
                orgs = []
                for org in org_data:
                    orgs.append({
                        'entity' : entity.id,
                        'organization_type' : org
                    })

                org_serializer = OrganizationTypeSerializer(data=orgs, many=True)
                org_serializer.is_valid(raise_exception=True)
                org_serializer.save()

        return entity

    def update(self, instance, validated_data):
        """Override to update Entity and OrganizationType objects with extra content
        passed in context.
        Extra data:
            * organization_type (list) : list of strings containing the organization sphere
        of action.
        """
        with transaction.atomic():
            org_data = self.context['extra'].get('organization_type', [])
            # substitute the organization_type 
            if len(org_data) != 0:
                orgs_qs = OrganizationType.objects.filter(entity=instance)
                for org in orgs_qs:
                    org.delete()

                orgs = []
                for org in org_data:
                    orgs.append({
                        'entity' : instance.id,
                        'organization_type' : org.organization_type
                    })
                orgs_serializer = OrganizationTypeSerializer(data=orgs, many=True)
                orgs_serializer.is_valid(raise_exception=True)
                orgs_serializer.save()

            instance.name = validated_data.get('name', instance.name)
            instance.save()
        return instance

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
        validated_data.pop('entity')
        with transaction.atomic():
            # create entity
            entity_data = self.context['extra'].get('entity', {})

            # create organization type
            entity_serializer = EntitySerializer(
                data={
                    'name' : entity_data.get('name', '')
                }, 
                context={
                    'extra' : {
                        'organization_type' : entity_data.get('organization_type', [])
                }
            })
            entity_serializer.is_valid(raise_exception=True)
            entity = entity_serializer.save()

            # create databreach object
            databreach = DataBreach.objects.create(**validated_data, entity=entity)

            # create sources
            source_data = self.context['extra'].get('sources', [])
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

    def update(self, instance, validated_data):
        """Override to update a DataBreach object. Needs to receive the id
        of the instance. that needs to be updated.
        """
        with transaction.atomic():
            request_data = self.context['request'].data
            instance.year = request_data.get('year', instance.year)
            instance.records = request_data.get('records', instance.records)
            instance.method = request_data.get('method', instance.method)

            entity = instance.entity
            if 'entity' in request_data:
                entity_serializer = EntitySerializer(
                    data={
                        'name' : request_data['entity']['name']
                    }, 
                    context={
                        'extra' : {
                            'organization_type' : request_data['entity']['organization_type']
                    }
                })
                entity_serializer.is_valid(raise_exception=True)
                instance.entity = entity_serializer.save()
                instance.save()

        return instance
