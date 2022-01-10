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
            for databreach in data:
                try:
                    entity_data = databreach.pop('entity')
                    sources_data = databreach.pop('sources')

                    entity, created = Entity.objects.get_or_create(name=entity_data['name'])
                    if created:
                        entity.save()

                    for t in entity_data['organization_type']:
                        ot_data = {
                            'organization_type': t,
                            'entity': entity.id
                        }
                        ot, created = OrganizationType.objects.get_or_create(organization_type=t, entity=entity)
                        if created:
                            ot.save()

                    dtbreach = DataBreach(
                        year=databreach['year'],
                        records=databreach['records'],
                        method=databreach['method'],
                        entity=entity
                    )
                    dtbreach.save()

                    for s in sources_data:
                        source = Source(url=s, data_breach=dtbreach)
                        source.save()
                except Exception as e:
                    print("Not possible to register databreach "+str(databreach)+
                          " Error: "+str(e))
