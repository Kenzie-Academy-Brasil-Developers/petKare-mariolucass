from rest_framework import serializers

from .models import PetSex

from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=10)
    age = serializers.IntegerField()
    weight = serializers.FloatField()

    sex = serializers.ChoiceField(
        choices=PetSex.choices,
        default=PetSex.DEFAULT,
    )

    group = GroupSerializer()
    traits = TraitSerializer(many=True)
