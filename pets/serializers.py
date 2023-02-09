from rest_framework import serializers


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=10)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField(max_length=20, default="Not informed")
