from rest_framework import serializers
from example.models import File
from django_q.models import OrmQ


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("filename", "file")


class DjangoQSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrmQ
        fields = ("id", "lock")
