from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    file = serializers.FileField()
    folder = serializers.PrimaryKeyRelatedField(queryset=None, allow_null=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    shared_with = serializers.PrimaryKeyRelatedField(many=True, queryset=None, allow_null=True)
