from django.shortcuts import render


from rest_framework import generics, status
from rest_framework.response import Response
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
        data = super(FooDetail, self).metadata(request)
        data['allowed_methods'] = ['GET', 'PUT', 'PATCH', 'DELETE']
        return data


class FooListBad(generics.GenericAPIView):
    serialzier_class = FooSerializer
    model = Foo

    def get(self, request):
        return Reponse({'detail': "unauthorized errors bro"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        return Response({'detail': 'bad request bro'}, status=status.HTTP_400_BAD_REQUEST)

    def metadata(self, request):
        data = super(FooListBad, self).metadata(request)
        data['allowed_methods'] = ['GET', 'POST']
        return data


class FooDetailBad(generics.GenericAPIView):
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

    def metadata(self, request):
        data = super(FooDetailBad, self).metadata(request)
        data['allowed_methods'] = ['GET', 'PUT', 'PATCH', 'DELETE']
        return data

