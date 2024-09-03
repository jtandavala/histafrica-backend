from rest_framework import serializers

from histafrica.shared.application.dto import PaginationOutput


class UUIDSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class PaginationSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    last_page = serializers.IntegerField()


class ResourceSerializer(serializers.Serializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {"data": data}


class CollectionSerializer(serializers.ListSerializer):
    paginationOutput: PaginationOutput
    many = False

    def __init__(self, instance: PaginationOutput = None, **kwargs):
        if isinstance(instance, PaginationOutput):
            kwargs["instance"] = instance.items
            self.pagination = instance
        else:
            raise TypeError("instance must be a PaginationOutput")
        super().__init__(**kwargs)
