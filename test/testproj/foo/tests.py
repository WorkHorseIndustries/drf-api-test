from django.core.urlresolvers import reverse
from rest_framework import status
from drf_api_test import test
from .models import Foo


class ListAPITest(test.RESTTestCase):
    uri = reverse('foo')
    payload = {'bar': 'wat'}

    def setUp(self):
        Foo.objects.create(bar='nam')


class DetailAPITest(test.RESTTestCase):
    payload = {'bar': 'wat'}
    uri = reverse('foo_detail', kwargs={'pk': 1})

    def setUp(self):
        f = Foo.objects.create(**self.payload)
        self.uri = reverse('foo_detail', kwargs={'pk': f.pk})

