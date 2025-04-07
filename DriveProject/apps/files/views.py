from rest_framework import generics, permissions
from rest_framework.response import Response

from DriveProject.apps.files.serializers import FileSerializer, FolderSerializer


class File(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        folder_id = self.request.query_params.get('folder')
        if folder_id:
            files_queryset = self.request.user.files.filter(folder__id=folder_id)
            folders_queryset = self.request.user.folders.filter(parent__id=folder_id)
        else:
            files_queryset = self.request.user.files.all()
            folders_queryset = self.request.user.folders.filter(parent__isnull=True)

        files_serializer = FileSerializer(files_queryset, many=True)
        folders_serializer = FolderSerializer(folders_queryset, many=True)

        combined_response = {
            'files': files_serializer.data,
            'folders': folders_serializer.data
        }

        return Response(combined_response)

class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.files.all()


class FileShare(generics.UpdateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.files.all()


class FileUnshare(generics.UpdateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.files.all()


class FileDownload(generics.RetrieveAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.files.all()
