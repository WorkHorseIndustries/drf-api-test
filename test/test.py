import mock

from rest_framework import status
from drf_api_test import test

test_options_payload = {
    'name': 'login',
    'description' : 'this mocks a login options call',
    'renderers' : [],
    'parsers': [],
    'actions': {
        'POST' : {
            'username': {'type': 'string', 'required': True, 'readonly': False},
            'password': {'type': 'string', 'required': True, 'readonly': False}
        },
    },
    'allowed_methods': ['POST'],
}

class FakeResponse():
    status_code = None
    content = None
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

@mock('APIClient.options', test_options_payload)
@mock('APIClient.post', FakeResponse(status.HTTP_201_OK, "It's all good bro."))
class POSTTest(test.APIRESTTest):
    uri = 'v1/test'
    payload = {'username': 'test', 'password' : 'you will never guess it.'}


