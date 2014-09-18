from django.shortcuts import render


from rest_framework import generics
from .serializer import FooSerializer


class FooList(generics.ListCreateView):
    serializer_class = FooSerializer

    def metadata(self, request):
        data = super(FooList, self).metadata(request)
        data['allowed_methods'] = ['GET', 'POST']
        return data
