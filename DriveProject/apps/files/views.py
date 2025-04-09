from rest_framework import generics, permissions
from rest_framework.response import Response

from DriveProject.apps.files.serializers import FileSerializer, FolderSerializer, CreateFileSerializer, \
    DownloadFileSerializer, CreateFolderSerializer


class File(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        folder_id = self.kwargs.get('pk')
        if folder_id:
            files_queryset = self.request.user.files.filter(folder__id=folder_id)
            folders_queryset = self.request.user.folders.filter(parent__id=folder_id)
        else:
            files_queryset = self.request.user.files.filter(folder__isnull=True)
            folders_queryset = self.request.user.folders.filter(parent__isnull=True)

        files_serializer = FileSerializer(files_queryset, many=True)
        folders_serializer = FolderSerializer(folders_queryset, many=True)

        combined_response = files_serializer.data + folders_serializer.data

        return Response(combined_response)


class FileCreate(generics.CreateAPIView):
    serializer_class = CreateFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.files.all()


class FileDownload(generics.RetrieveAPIView):
    serializer_class = DownloadFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.files.all()


class Folder(generics.CreateAPIView):
    serializer_class = CreateFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class FolderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.folders.all()
