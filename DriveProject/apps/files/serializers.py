from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import serializers

from DriveProject.apps.files.models import Folder, File


class FileSerializer(serializers.Serializer):
    """
    Serializer for handling file-related data, including validation and transformation.
    """
    name: serializers.CharField = serializers.CharField(max_length=255)
    file: serializers.FileField = serializers.FileField()
    folder: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(), allow_null=True
    )
    owner: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    shared_with: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), allow_null=True
    )


class FolderSerializer(serializers.Serializer):
    """
    Serializer for a folder-like structure, defining how folder data should be
    serialized and deserialized, including fields for the folder's name, parent
    folder, owner, subfolders, and files.
    """
    name: serializers.CharField = serializers.CharField(max_length=255)
    parent: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(), allow_null=True
    )
    owner: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    subfolders: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Folder.objects.all(), allow_null=True
    )
    files: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        many=True, queryset=File.objects.all(), allow_null=True
    )


class FileShareSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    folder_id = serializers.IntegerField()


class FileUnshareSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    folder_id = serializers.IntegerField()


class FileDownloadSerializer(serializers.Serializer):
    """
    Serializer for handling file download-related data.
    """
    file_id: int = serializers.IntegerField()
    folder_id: int = serializers.IntegerField()
    file = serializers.FileField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    shared_with = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), allow_null=True
    )
    name: str = serializers.CharField(max_length=255)

