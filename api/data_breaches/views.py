from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import *
from .serializers import *

class DataBreachViewSet(viewsets.ModelViewSet):
    """
    ViewSet with CRUD and list functions from data breaches.
    """
    queryset = DataBreach.objects.all()
    serializer_class = DataBreachSerializer

    def get_serializer_context(self):
        """
        Pass extra content to DataBreachSerializer using request context.
        """
        context = super(DataBreachViewSet, self).get_serializer_context()
        context.update({
            "request" : self.request
        })
        return context
