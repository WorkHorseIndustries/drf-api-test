# TODO output writer

# TODO replace Asserts with equal checks then call output_writer and finally 
# fail test

# TODO add mock support

class PostTestMixin(object):

    def testFullPost(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            "POST to {0} with {1}\n returned: ".format(self.url, 
                                    self.payload response.content))

    def testBadPost(self):
        for required_field_key in self.required_fields:
            payload = self.payload.copy()
            payload.pop(required_field_key)
            response = self.client.post(self.url, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 
                """POST to {0} with {1} where required field: {2} is omitted.\
                \nreturned: {3}""".format(self.url, self.payload,
                                     required_field_key, response.content))

    def testPartialPost(self):
        for optional_field_key in self.optional_fields:
            payload = self.payload.copy()
            payload.pop(optional_field_key)
            response = self.client.post(self.url, payload)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, 
                """POST to {0} with {1] where optional field: {1} is omitted\
                \nreturn: {3}""".format(self.url, self.payload, 
                                        optional_field_key, response.content)})


class PutTestMixin(object):
    
    def testFullPut(self):
        response = self.client.put(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            "PUT to {0} with {1}\n returned: ".format(self.url, 
                                    self.payload response.content))

    def testBadPut(self):
        for required_field_key in self.required_fields:
            payload = self.payload.copy()
            payload.pop(required_field_key)
            response = self.client.put(self.url, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                """PUT to {0} with {1} where required field: {2} is omitted.\
                \nreturned: {3}""".format(self.url, self.payload,
                                     required_field_key, response.content))

    def testPartialPut(self):
        for optional_field_key in self.optional_fields:
            payload = self.payload.copy()
            payload.pop(optional_field_key)
            response = self.client.put(self.url, payload)
            self.assertEqual(response.status_code, status.HTTP_200_OK,
                """PUT to {0} with {1] where optional field: {1} is omitted\
               \nreturn: {3}""".format(self.url, self.payload, 
                                        optional_field_key, response.content)})
    

class PatchTestMixin(object):

    def testPatch(self):
        response = self.client.patch(self.url, self.payload)
        self.assertEqual(resposne.status_code, status.HTTP_200_OK, 
            "PATCH to {0} with {1} \nreturned:{3}".format(self.url, 
                                            self.payload, response.content))


class DeleteTestMixin(object):
    
    def testDelete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            "DELETE to {0}"format(self.url))
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            "After initial DELETE second DELETE to {0} \nreturned: ".format(
                                                    self.url, response.content))


class GetTestMixin(object):
    
    def testGet(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            "GET to {0} \nreturned:{1}".format(self.url, response.content)

