Django RESTful TestCase
=======================

Use the HTTP OPTIONS method to detect the capabilities of an endpoint and run basic tests against it for each HTTP method allowed by that endpoint. 


##Example

```python 
from drf_api_test import test 

YourTestCase(test.RESTTestCase):
    uri = reverse(your_view)
    payload = {} 


    def setUp(self):
        pass
```

##Instructions 

When a TestCase inherits from RESTTestCase You must provide a uri which will be used by django-rest-frameworks APITestClient to access your view.  You must also provide a payload object if your resource implements either the POST, PUT or PATCH method(s). If you endpoint Implements either GET or DELETE method(s) the setUp for your TestCase must ensure that an object exists at that endpoint to be retrieved or deleted. 

