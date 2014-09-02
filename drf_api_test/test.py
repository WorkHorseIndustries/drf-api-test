from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .mixins import PostMixin, PutMixin, PatchMixin, DeleteMixin, GetMixin


def create_resource_func(url, payload):
    response = self.client.post(self.url, self.payload)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "Resource create POST to {0} with {1}\n returned:".format(self.url, 
                                                self.payload response.content))

class MetaAPITest(type):
    def __new__(cls, name, bases, attrs):
        method_mixins = {
            'POST': PostMixin,
            'PUT': PutMixin,
            'PATCH': PatchMixin,
            'DELETE': DeleteMixin,
            'GET': GetMixin
        }
        class_mixins = []
        ep = attrs.get('endpoints', '')
        client = APIClient()
        print client.options(ep)
        mixins = [method_mixins[method] for method in client.options(ep)]
        class_mixins.append(mixins)
        bases = bases + tuple(set(class_mixins))

        if PostMixin in mixins and not 'create_resource' in attrs:
            attrs['create_resource'] = create_resource_func

        return super(MetaAPITest, cls).__new__(cls, name, bases, attrs)


class APITest(APITestCase):
    __metaclass__ = MetaAPITest 
    url = ''
    payload = {}
    required_fields = []
    optional_fields = []
    

    
    
