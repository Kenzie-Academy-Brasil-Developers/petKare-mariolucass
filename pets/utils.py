from groups.models import Group
from traits.models import Trait
from rest_framework.views import Response, status


class PetMethods:
    def find_group(group):
        try:
            group_find = Group.objects.get(scientific_name=group["scientific_name"])
        except Group.DoesNotExist:
            group_find = Group.objects.create(**group)
        return group_find

    def find_traits(traitsParams):
        traits = []

        for trait in traitsParams:
            trait_find = Trait.objects.filter(name__iexact=trait["name"]).first()

            if not trait_find:
                trait_find = Trait.objects.create(**trait)

            traits.append(trait_find)

        return traits

    def update_keys(keys, pet):
        for key, value in keys:
            if key != id:
                setattr(pet, key, value)


class ResponseMethods:
    def generate_response_success(status_code, variant="Deleted method"):
        match status_code:
            case 200:
                status_code = status.HTTP_200_OK
            case 201:
                status_code = status.HTTP_201_CREATED
            case 204:
                status_code = status.HTTP_204_NO_CONTENT
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(variant, status_code)
