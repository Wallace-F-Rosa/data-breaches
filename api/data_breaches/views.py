from django.shortcuts import render
from rest_framework import viewsets, response, status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import TokenAuthentication
from .models import *
from .serializers import *

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class DataBreachViewSet(viewsets.ModelViewSet):
    """
    ViewSet with CRUD and list functions from data breaches.

    To create, update and delete data breaches you need to pass the api-key
    under the "Authorization" request header preceded by the string 'Api-Key'.
    Example:

    ```code
    Authorization: Api-Key uxUQHQyq.y9idPHRxbcYNzQriuwAbkYC3fBupq6vw
    ```

    To create a data breach you need to pass what entity is involved
    (organization_type is an option field describing the organization's sphere
    of action), the year of the breach, the amount of data records breached,
    the method used and the sources abourding the breach. 

    Example:

    ```json
    {
            "entity": {
                "name": "21st Century Oncology",
                "organization_type": [
                    "healthcare"
                ]
            },
            "year": "2016",
            "records": 2200000,
            "method": "hacked",
            "sources": [
                "https://gizmodo.com/mother-of-all-breaches-exposes-773-million-emails-21-m-1831833456",
                "http://cbs12.com/news/local/21st-century-oncology-notifies-22-million-of-hacking-data-breach"
            ]
    }
    ```
    """
    queryset = DataBreach.objects.all()
    serializer_class = DataBreachSerializer
    permission_classes = [HasAPIKey | IsAuthenticated | ReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_context(self):
        """Pass extra content to DataBreachSerializer using request context.
        The data is passed as 'extra' dict.
        """
        context = super(DataBreachViewSet, self).get_serializer_context()
        entity_data = self.request.data.get('entity', None)
        extra_data = {
        }
        if entity_data:
            extra_data['entity'] = entity_data
        sources_data = self.request.data.get('sources', None)
        if sources_data:
            extra_data['sources'] = sources_data
        context.update({
            'extra' : extra_data
        })
        return context

    def destroy(self, request, *args, **kwargs):
        """Override to delete sources when data breach is deleted."""
        instance = self.get_object()
        with transaction.atomic():
            sources = Source.objects.filter(data_breach=instance)
            for s in sources:
                s.delete()
            self.perform_destroy(instance)

        return response.Response(status=status.HTTP_204_NO_CONTENT)
