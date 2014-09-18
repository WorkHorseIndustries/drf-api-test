from rest_framework import serializers
from .models import Foo


class FooSerializer(serializers.ModelSerialzer):

    class Meta():
        model = Foo
        fields = ('bar')

