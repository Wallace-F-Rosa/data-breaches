import argparse
import json
from data_breaches.serializers import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Populate database with data breaches data from a json file."

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str, help="Path to the json file with data breaches data.")

    def handle(self, *args, **options):
        json_path = options['json_path']
        with open(json_path, 'r') as jsonf:
            data = json.load(jsonf)
            serializer = DataBreachSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
