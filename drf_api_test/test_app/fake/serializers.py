from rest_framework import serializers
from .models import Fake


class FakeSerializer(serializers.ModelSerializer):

    class Meta():
        model = Fake
