from rest_framework import generics, permissions

from DriveProject.apps.files.serializers import FileSerializer


class FileList(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.request.user.files.all()
        folder_id = self.request.query_params.get('folder')
        if folder_id:
            queryset = queryset.filter(folder__id=folder_id)
        return queryset


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

