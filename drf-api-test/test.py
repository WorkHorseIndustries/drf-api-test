from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework.test import APIClient
from rest_framework import status
from .mixins import PostMixin, PutMixin, PatchMixin, DeleteMixin, GetMixin


class InvalidClientError(Exception):
    pass


class MetaAPITest(type):
    def __new__(cls, name, bases, attrs):
        method_mixins = {
            'POST': PostMixin,
            'PUT': PutMixin,
            'PATCH': PatchMixin,
            'DELETE': DeleteMixin,
            'GET': GetMixin
        }
        client = APIClient()
        class_mixins = []
        for ep in attrs.get('endpoints', []):
            mixins = [method_mixins[method] for method in client.options(endpoint)]
            class_mixins.append(mixins)
        bases = bases + tuple(set(class_mixins))
        return super(MetaAPITest, cls).__new__(cls, name, bases, attrs)


class APITest(TestCase):
    __metaclass__ = MetaAPITest 

    endpoints = []
    client = APIClient()
    payload = {}
    required_fields = []
    optional_fields = []
    # TODO: look up if you can get the name of the reverse from the url
    def __init__(self, endpoints, client=None, payload={}, 
        required_fields=[], optional_fields=[]):
        
        if not client:
            client = APIClient()
        elif client is not APIClient:
            raise InvalidClientError("""client is not an instance of \
                                        rest_framework.test.APIClient""")

    

    
    
