from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from DriveProject.apps.files.models import Folder, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'modified_at', 'size', 'type')


class DownloadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_url']


class CreateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class FolderSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('id', 'name', 'modified_at', 'type', 'size')

    def get_type(self, obj):
        return 'folder'


class CreateFolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('name', 'parent')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


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
