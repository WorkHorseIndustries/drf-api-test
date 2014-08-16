from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework.test import APIClient
from rest_framework import status
from .mixins import PostMixin, PutMixin, PatchMixin, DeleteMixin, GetMixin


class InvalidClientError(Exception):
    pass

class APITestWriter(object):
    
    client = APIClient()
    method_mixins = {
        'POST': PostMixin,
        'PUT': PutMixin,
        'PATCH': PatchMixin,
        'DELETE': DeleteMixin,
        'GET': GetMixin
    }

    # TODO: look up if you can get the name of the reverse from the url
    def __init__(self, endpoints, client=None, payload={}, 
        required_fields=[], optional_fields=[]):
        
        class_mixins = []
        for ep in endpoints:
            class_mixins.append(ep)

        if not client:
            client = APIClient()
        elif client is not APIClient:
            raise InvalidClientError("""client is not an instance of \
                                        rest_framework.test.APIClient""")

    def _get_mixins(self, enpoint):

        allowed_methods = self.client.options(endpoint)
        mixins = [self.method_mixins[method] for method in allowed_methods]
        return mixins

    def write_cls(ep, payload, client, required_fields, optional_fields):
        pass
    


