import StringIO
import json
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# TODO mixins should be class generators so we can add dynamic data to them
# such as expected status_codes and payload comparitors. 


def _error_message(actual_status, expected_status, method, uri, payload, response_content, details=''):
    msg = '{0} is not expected {1}\n'
    msg += "{0}: {1}\n".format(method, uri)
    msg += "payload: {2}\nresponse content: {3}\n"
    if details:
        msg += "details: " + details
    return msg.format(actual_status, expected_status, payload, response_content)


class PostTestMixin(APITestCase):

    def testFullPost(self):
        response = self.client.post(self.uri, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                _error_message(response.status_code, status.HTTP_201_CREATED, "POST", self.uri,
                    self.payload, response.content))

    def testBadPost(self):
        for required_field_key in self.required_fields:
            payload = self.payload.copy()
            payload.pop(required_field_key)
            response = self.client.post(self.uri, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                   _error_message(response.status_code, status.HTTP_400_BAD_REQUEST,
                        "POST", self.uri, payload, response.content,
                        "Intentionally ommited required field {0}".format(required_field_key)))

    def testPartialPost(self):
        for optional_field_key in self.optional_fields:
            payload = self.payload.copy()
            payload.pop(optional_field_key, None)
            response = self.client.post(self.uri, payload)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                 _error_message(response.status_code, status.HTTP_201_CREATED, "POST", self.uri, payload,
                     response.content, "intentionall omitted optional field {}".format(optional_field_key)))


class PutTestMixin(APITestCase):

    def testFullPut(self):
        response = self.client.put(self.uri, self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            _error_message(response.status_code, status.HTTP_200_OK,
                "PUT", self.uri, self.payload, response.content))


    def testBadPut(self):
        for required_field_key in self.required_fields:
            payload = self.payload.copy()
            payload.pop(required_field_key)
            response = self.client.put(self.uri, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                 _error_message(response.status_code, status.HTTP_400_BAD_REQUEST,
                        "PUT", self.uri, payload, response.content,
                        "Intentionally ommited required field {0}".format(required_field_key)))

    def testPartialPut(self):
        for optional_field_key in self.optional_fields:
            payload = self.payload.copy()
            payload.pop(optional_field_key, None)
            response = self.client.put(self.uri, payload)
            self.assertEqual(response.status_code, status.HTTP_200_OK,
               _error_message(response.status_code, status.HTTP_200_OK, "PUT", self.uri, payload,
                     response.content, "intentionall omitted optional field {}".format(optional_field_key)))




class PatchTestMixin(APITestCase):

    def testPatch(self):
        response = self.client.patch(self.uri, self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
             _error_message(response.status_code, status.HTTP_200_OK, "PATCH", self.uri,
                    self.payload, response.content))


class DeleteTestMixin(APITestCase):

    def testDelete(self):
        response = self.client.delete(self.uri)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            _error_message(response.status_code, status.HTTP_204_NO_CONTENT,
                "DELETE", self.uri, "", response.content))

        response = self.client.delete(self.uri)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            _error_message(response.status_code, status.HTTP_404_NOT_FOUND,
                "DELETE", self.uri, "", response.content,
                "Second DELETE resource should have been deleted"))

class GetTestMixin(APITestCase):

    def testGet(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            _error_message(response.status_code, status.HTTP_200_OK, "GET",
                self.uri, "", response.content))

class HttpOptionsFormatError(Exception):
    pass


class MetaRESTTest(type):

    def __new__(cls, name, bases, attrs):
        class_mixins = []
        uri = attrs.get('uri', None)
        if uri:
            client = APIClient()
            options_metadata = json.load(StringIO.StringIO(client.options(uri).content))

            if not options_metadata.get('allowed_methods'):
                raise HttpOptionsFormatError(
                """options didn't return a list of 'allowed_methods' http methods. Consider overriding \
                    the metadata method on this view \
                    http://www.django-rest-framework.org/topics/documenting-your-api .\
                    add 'allowed' to the returned dict which should contain a list of all HTTP \
                    supported by this endpoint.""")

            method_mixins = attrs.pop('method_mixins', None)

            if not method_mixins:
                for base in bases:
                    try:
                        method_mixins = base.method_mixins
                    except:
                        pass

            class_mixins += ([method_mixins[method] for method
                    in options_metadata['allowed_methods'] if method in method_mixins])

            print name
            print options_metadata['allowed_methods']
            if 'actions' in options_metadata:
                fields_data = options_metadata['actions'].get(
                                        'POST', options_metadata['actions'].get('PUT'))
                if fields_data is None:
                    raise HttOptionsFormatError("actions included in response but didn't \
                        contain either POST or PUT action metadata")

                attrs['required_fields'] = []
                attrs['optional_fields'] = []
                for k,v  in fields_data.iteritems():
                    if v['required']:
                        field_list = 'required_fields'
                    else:
                        field_list = 'optional_fields'
                    attrs[field_list].append(k)
            bases += tuple(class_mixins)
        return super(MetaRESTTest, cls).__new__(cls, name, bases, attrs)


class RESTTestCase(APITestCase):
    __metaclass__ = MetaRESTTest
    uri = None
    required_fields = []
    optional_fields = []
    method_mixins = {
        'POST': PostTestMixin,
        'PUT': PutTestMixin,
        'PATCH': PatchTestMixin,
        'DELETE': DeleteTestMixin,
        'GET': GetTestMixin
    }

