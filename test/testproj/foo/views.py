from django.shortcuts import render


from rest_framework import generics
from .serializers import FooSerializer
from .models import Foo

class FooList(generics.ListCreateAPIView):
    serializer_class = FooSerializer
    model = Foo

    def metadata(self, request):
        data = super(FooList, self).metadata(request)
        data['allowed_methods'] = ['GET', 'POST']
        return data

class FooDetail(generics.RetrieveUpdateDestroyAPIView):
    serialzier_class = FooSerializer
    model = Foo
    def metadata(self, request):
        print "here"
        data = super(FooDetail, self).metadata(request)
        data['allowed_methods'] = ['GET', 'PUT', 'PATCH', 'DELETE']
        return data
