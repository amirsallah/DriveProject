from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from DriveProject.apps.files.models import Folder, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'modified_at', 'size', 'type')


class EditFileSerializer(serializers.ModelSerializer):
    unshared_with_ids = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = File
        fields = ('name', 'folder', 'shared_with', 'unshared_with_ids')

    def update(self, instance, validated_data):
        shared_with_ids = validated_data.get('shared_with', [])
        unshared_with_ids = validated_data.get('unshared_with_ids', [])

        instance = super().update(instance, validated_data)

        if shared_with_ids:
            for user_id in shared_with_ids:
                instance.add_user_to_share_list(user_id)
        if unshared_with_ids:
            for user_id in unshared_with_ids:
                instance.remove_user_to_share_list(user_id)

        return instance


class DownloadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_url']


class CreateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file', 'folder']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class FolderSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('id', 'name', 'modified_at', 'type', 'size', 'parent')

    def get_type(self, obj):
        return 'folder'

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name
        return None


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
