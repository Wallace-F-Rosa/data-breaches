from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *

# Create your tests here.
class DataBreachTestCase(APITestCase):
    """Test case for CRUD and list functionalities on data breaches."""
    def setUp(self):
        # TODO: add data breaches required to test. search some on https://en.wikipedia.org/wiki/List_of_data_breaches.
        self.list_url = reverse('databreaches-list')

    def compareDataBreaches(self, dt0, dt1):
        """Compare two databreaches json data.

        Args:
            dt0 (dict) : dictionary containing json data of a data breach.
            dt1 (dict) : dictionary containing json data of a data breach.

        Return:
            Returns True if data breaches have the same entity, records, year,
        , method and sources. False is returned otherwise.
        """
        fields = ['entity',  'year', 'records', 'method', 'sources']
        for field in fields:
            if dt0[field] != dt1[field]:
                return False

        return True

    def test_list(self):
        """Testing update action of /databreaches endpoint. This action
        should list all databreaches available.
        """
        # add some data breaches
        list_url = self.list_url

        data = [
                {
                    "entity": {
                        "name": "21st Century Oncology",
                        "organization_type": [
                            "healthcare"
                        ]
                    },
                    "year": 2016,
                    "records": 2200000,
                    "method": "hacked",
                    "sources": [
                        "https://gizmodo.com/mother-of-all-breaches-exposes-773-million-emails-21-m-1831833456",
                        "http://cbs12.com/news/local/21st-century-oncology-notifies-22-million-of-hacking-data-breach"
                    ]
                },
                {
                    "entity": {
                        "name": "500px",
                        "organization_type": [
                            "social networking"
                        ]
                    },
                    "year": 2020,
                    "records": 14870304,
                    "method": "hacked",
                    "sources": [
                        "http://www.natlawreview.com/article/oh-no-not-again-chalk-yet-another-health-data-breach"
                    ]
                }
        ]

        for dt in data:
            response = self.client.post(list_url, dt, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        response = self.client.get(list_url)
        self.assertEqual(len(response.data), 2)
        for i in range(len(data)):
            self.assertTrue(self.compareDataBreaches(data[i], response.data[i]), "Data is different !\nOriginal Data : " + str(data[i]) + '\nReponse from API: ' + str(response.data[i]))


    def test_create(self):
        """Testing create action of /databreaches endpoint on:
            * Successfull case
            * Request missing data
            * Request containing invalid fields
        """
        # successfull case
        create_url = self.list_url
        data = {
            'entity' : {
                'name' : 'Test'
            },
            'year' : 2021,
            'records' : 10000,
            'method' : 'hacking',
            'sources' : ['https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal']
        }
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        
        # dont duplicate entity
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        entity_count = Entity.objects.filter(name=data['entity']['name']).count()
        self.assertEqual(entity_count, 1)
        
        # request missing data
        data = {
            'year' : '2021',
            'recors' : 10000,
            'method' : 'hacking',
            'sources' : ['https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal']
        }
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # request with invalid data
        data = {
            'entity' : {
                'name' : 'Test',
                'organization_type' : ['web']
            },
            'year' : '2021',
            'recors' : -120,
            'method' : 'hacking',
            'sources' : ['https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal']
        }
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        """Test update of data breaches data. Cover the cases below:
            * Valid update
            * Request containing invalid fields
        """
        # criar objetos
        data = [
                {
                    "entity": {
                        "name": "21st Century Oncology",
                        "organization_type": [
                            "healthcare"
                        ]
                    },
                    "year": 2016,
                    "records": 2200000,
                    "method": "hacked",
                    "sources": [
                        "https://gizmodo.com/mother-of-all-breaches-exposes-773-million-emails-21-m-1831833456",
                        "http://cbs12.com/news/local/21st-century-oncology-notifies-22-million-of-hacking-data-breach"
                    ]
                },
                {
                    "entity": {
                        "name": "500px",
                        "organization_type": [
                            "social networking"
                        ]
                    },
                    "year": 2020,
                    "records": 14870304,
                    "method": "hacked",
                    "sources": [
                        "http://www.natlawreview.com/article/oh-no-not-again-chalk-yet-another-health-data-breach"
                    ]
                }
        ]

        create_url = self.list_url
        for i in range(len(data)):
            response = self.client.post(create_url, data=data[i], format='json')
            data[i] = response.data
        
        # successfull update
        db_id = data[0]['id']
        update_url = reverse('databreaches-detail', args=[db_id])
        data[0]['entity'] = {
            'name' : 'Microsoft',
            'organization_type' : ['software']
        }
        response = self.client.put(update_url, data=data[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        # request with invalid data
        data[1]['year'] = -1200
        response = self.client.put(update_url, data=data[1], format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_delete(self):
        pass


class MethodsTestCase(APITestCase):
    pass

