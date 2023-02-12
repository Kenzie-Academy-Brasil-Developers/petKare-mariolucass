from django.forms import model_to_dict
from rest_framework.views import APIView, Response, Request, status
from django.shortcuts import get_object_or_404

from rest_framework.pagination import PageNumberPagination

from .models import Pet
from .utils import PetMethods, ResponseMethods
from .serializers import PetSerializer


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        if request.query_params:
            traitName = request.query_params["trait"]
            pets = Pet.objects.filter(traits__name=traitName)

        else:
            pets = Pet.objects.all().order_by("id")

        result_page = self.paginate_queryset(pets, request, view=self)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pet = serializer.validated_data

        traitsBody = pet.pop("traits")
        groupBody = pet.pop("group")

        group = PetMethods.find_group(groupBody)
        pet = Pet.objects.create(**pet, group=group)

        traits = PetMethods.find_traits(traitsBody)
        pet.traits.set(traits)

        serializer = PetSerializer(pet)

        return ResponseMethods.generate_response_success(201, serializer.data)


class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return ResponseMethods.generate_response_success(200, serializer.data)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        pet_body = serializer.validated_data

        if "group" in pet_body:
            group_body = pet_body.pop("group")

            group = PetMethods.find_group(group_body)

            pet.group = group

        if "traits" in pet_body:
            traits_body = pet_body.pop("traits")

            traits = PetMethods.find_traits(traits_body)

            pet.traits.set(traits)

        PetMethods.update_keys(pet_body.items(), pet)

        pet.save()

        serializer = PetSerializer(pet)

        return ResponseMethods.generate_response_success(200, serializer.data)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        pet.delete()

        return ResponseMethods.generate_response_success(204)
