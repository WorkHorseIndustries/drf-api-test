from django.core.urlresolvers import reverse
from rest_framework import status
from drf_api_test import test

class ListAPITest(test.APIRESTTest):
    uri = reverse('foo')
    payload = {'bar': 'wat'}
