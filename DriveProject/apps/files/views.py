from rest_framework import generics, permissions
from rest_framework.response import Response

from DriveProject.apps.files.serializers import FileSerializer, FolderSerializer, CreateFileSerializer, \
    DownloadFileSerializer


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


class FileShare(generics.UpdateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return self.request.user.files.all()

    def update(self, request, *args, **kwargs):
        file = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=400)

        # Assuming you have a method to add a user to the file's share list
        file.add_user_to_share_list(user_id)
        file.save()

        serializer = self.get_serializer(file)
        return Response(serializer.data)


class FileUnshare(generics.UpdateAPIView):
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
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]


class FolderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.folders.all()
