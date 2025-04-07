from django.contrib.auth.models import User
from rest_framework import serializers

from DriveProject.apps.files.models import Folder, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'file', 'folder', 'owner', 'shared_with')


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('id', 'name', 'parent', 'owner', 'subfolders', 'files')


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
