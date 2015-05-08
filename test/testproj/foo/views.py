from django.shortcuts import render

from drf_api_test.mixins import OptionsAllowedMethodsMixin
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import FooSerializer
from .models import Foo

class FooList(OptionsAllowedMethodsMixin, generics.ListCreateAPIView):
    serializer_class = FooSerializer
    model = Foo

class FooDetail(OptionsAllowedMethodsMixin, generics.RetrieveUpdateDestroyAPIView):
    serialzier_class = FooSerializer
    model = Foo


class FooListBad(OptionsAllowedMethodsMixin, generics.GenericAPIView):
    serialzier_class = FooSerializer
    model = Foo

    def get(self, request):
        return Response({'detail': "unauthorized errors bro"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        return Response({'detail': 'bad request bro'}, status=status.HTTP_400_BAD_REQUEST)


class FooDetailBad(OptionsAllowedMethodsMixin, generics.GenericAPIView):
    serialzier_class = FooSerializer
    model = Foo

    def put(self, request, pk):
        return Response({'detail': 'bad request bro'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return Response({'detail': 'bad request bro'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        return Response({'detail': 'bad request bro'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        return Response({'detail': 'bad request bro'}, status=status.HTTP_401_UNAUTHORIZED)

