from django.contrib.auth.models import User
from rest_framework import serializers

from DriveProject.apps.files.models import Folder, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'modified_at', 'size', 'type')


class FolderSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('id', 'name', 'modified_at', 'type', 'size')

    def get_type(self, obj):
        return 'folder'

    # def get_size(self, obj):
    #     size_in_mb = obj.get_size() / (1024 * 1024)
    #     if size_in_mb < 1:
    #         return f"{obj.get_size()} bytes"
    #     return f"{size_in_mb:.2f} MB"


class FileShareSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    folder_id = serializers.IntegerField()


class FileUnshareSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    folder_id = serializers.IntegerField()


class FileDownloadSerializer(serializers.Serializer):
    file_id: int = serializers.IntegerField()
    folder_id: int = serializers.IntegerField()
    file = serializers.FileField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    shared_with = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), allow_null=True
    )
    name: str = serializers.CharField(max_length=255)
