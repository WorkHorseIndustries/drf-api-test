import StringIO
import json
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# TODO mixins should be class generators so we can add dynamic data to them
# such as expected status_codes and payload comparitors. 

class PostTestMixin(APITestCase):

    def testFullPost(self):
        response = self.client.post(self.uri, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "POST to {0} with {1}\n returned: {2}".format(self.uri,
                                    self.payload, response.content))

    def testBadPost(self):
        for required_field_key in self.required_fields:
            payload = self.payload.copy()
            payload.pop(required_field_key)
            response = self.client.post(self.uri, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                """POST to {0} with {1} where required field: {2} is omitted.\
                \nreturned: {3}""".format(self.uri, self.payload,
                                     required_field_key, response.content))

    def testPartialPost(self):
        for optional_field_key in self.optional_fields:
            payload = self.payload.copy()
            payload.pop(optional_field_key)
            response = self.client.post(self.uri, payload)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                """POST to {0} with {1] where optional field: {1} is omitted\
                \nreturn: {3}""".format(self.uri, self.payload,
                                        optional_field_key, response.content))


class PutTestMixin(APITestCase):

    def testFullPut(self):
        response = self.client.put(self.uri, self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            "PUT to {0} with {1}\n returned: {2}".format(self.uri,
                                    self.payload, response.content))

    def testBadPut(self):
        for required_field_key in self.required_fields:
            payload = self.payload.copy()
            payload.pop(required_field_key)
            response = self.client.put(self.uri, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                """PUT to {0} with {1} where required field: {2} is omitted.\
                \nreturned: {3}""".format(self.uri, self.payload,
                                     required_field_key, response.content))

    def testPartialPut(self):
        for optional_field_key in self.optional_fields:
            payload = self.payload.copy()
            payload.pop(optional_field_key)
            response = self.client.put(self.uri, payload)
            self.assertEqual(response.status_code, status.HTTP_200_OK,
                """PUT to {0} with {1] where optional field: {1} is omitted\
               \nreturn: {3}""".format(self.uri, self.payload,
                                        optional_field_key, response.content))


class PatchTestMixin(APITestCase):

    def testPatch(self):
        response = self.client.patch(self.uri, self.payload)
        self.assertEqual(resposne.status_code, status.HTTP_200_OK,
            "PATCH to {0} with {1} \nreturned: {2}".format(self.uri,
                                            self.payload, response.content))


class DeleteTestMixin(APITestCase):

    def testDelete(self):
        response = self.client.delete(self.uri)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            "DELETE to {0}".format(self.uri))
        response = self.client.delete(self.uri)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            "After initial DELETE second DELETE to {0} \nreturned: {1}".format(
                                                    self.uri, response.content))


class GetTestMixin(APITestCase):

    def testGet(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            "GET to {0} \nreturned:{1}".format(self.uri, response.content))


class HttpOptionsFormatError(Exception):
    pass


class MetaAPIRESTTest(type):

    def __new__(cls, name, bases, attrs):
        class_mixins = []
        uri = attrs.get('uri', None)
        print attrs
        if not uri:
            raise NotImplementedError("you must include a uri for an endpoint to test")

        client = APIClient()
        option_metadata = json.load(StringIO(client.options(uri)))

        if not options_metadata.get('allowed_methods'):
            raise HttpOptionsFormatError(
            """options didn't return a list of 'allowed_methods' http methods. Consider overriding \
                the metadata method on this view \
                http://www.django-rest-framework.org/topics/documenting-your-api .\
                add 'allowed' to the returned dict which should contain a list of all HTTP \
                supported by this endpoint.""")

        mixins = [method_mixin[method] for method
                in options_metadata['allowed'] if method in attrs.pop('method_mixins', {})]

        class_mixins.append(mixins)

        if 'actions' in options_metatadata:
            fields_data = options_metadata['actions'].get(
                                    'POST', options_metatadata['actions'].get('PUT'))
            if field_data is None:
                raise HttOptionsFormatError("actions included in resposne but didn't \
                    contain either POST or PUT action metadata")

            for k,v  in fields_data.iteritems():
                if v['required']:
                    field_list = 'required_fields'
                else:
                    field_list = 'optional_fields'
                attrs[field_list] = attrs[fields_list].append(k)

        bases = bases + tuple(set(class_mixins))

        return super(MetaAPITest, cls).__new__(cls, name, bases, attrs)


class APIRESTTest(APITestCase):
    __metaclass__ = MetaAPIRESTTest
    # uri = None
    # payload = None
    # required_fields = []
    # optional_fields = []
    method_mixins = {
        'POST': PostTestMixin,
        'PUT': PutTestMixin,
        'PATCH': PatchTestMixin,
        'DELETE': DeleteTestMixin,
        'GET': GetTestMixin
    }
