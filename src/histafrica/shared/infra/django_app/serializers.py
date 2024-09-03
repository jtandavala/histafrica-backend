from rest_framework import serializers


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
