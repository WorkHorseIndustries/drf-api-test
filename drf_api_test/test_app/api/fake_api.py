from rest_framework import generics


from fake.serializers import FakeSerializer
from fake.models import Fake


class FakeListCreateView(generics.ListCreateAPIView):
    model = Fake
    serializer_class = FakeSerializer


class FakeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    model = Fake
    serializer_class = FakeSerializer
