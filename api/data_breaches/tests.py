from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

# Create your tests here.
class DataBreachTestCase(APITestCase):
    """Test case for CRUD and list functionalities on data breaches."""
    def setUp(self):
        pass
        # TODO: add data breaches required to test. search some on https://en.wikipedia.org/wiki/List_of_data_breaches.

    def test_list(self):
        pass

    def test_create(self):
        """Testing create action of /databreaches endpoint on:
            - Successfull case
            - Request missing data
            - Request containing invalid fields
        """
        # successfull case
        create_url = reverse('databreaches-list')
        data = {
            'entity' : 'Test',
            'year' : '2021',
            'recors' : 10000,
            'organization_type' : 'web',
            'method' : 'hacking',
            'sources' : ['https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal']
        }
        response = self.client.post(create_url, json.dumps(data), format=json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # request missing data
        create_url = reverse('databreaches-list')
        data = {
            'year' : '2021',
            'recors' : 10000,
            'organization_type' : 'web',
            'method' : 'hacking',
            'sources' : ['https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal']
        }
        response = self.client.post(create_url, json.dumps(data), format=json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # request with invalid data
        data = {
            'entity' : 'Test',
            'year' : '2021',
            'recors' : 10000,
            'organization_type' : 'web',
            'method' : 'hacking',
            'sources' : ['https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal']
        }
        response = self.client.post(create_url, json.dumps(data), format=json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        pass

    def test_delete(self):
        pass


class MethodsTestCase(APITestCase):
    pass

