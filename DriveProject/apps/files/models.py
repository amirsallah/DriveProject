import mimetypes

from django.contrib.auth.models import User
from django.db import models

from DriveProject.apps.core.models import CreationModificationDateAbstractModel


class Folder(CreationModificationDateAbstractModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='folders', on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shared_folders', blank=True)
    size = models.BigIntegerField(null=True, blank=True)

    def get_size(self):
        size = 0
        print(self.files.all())
        for file in self.files.all():
            if file.size:
                size += file.size

        for subfolder in self.subfolders.all():
            size += subfolder.get_size()

        return size

    def save(self, *args, **kwargs):
        self.size = self.get_size()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class File(CreationModificationDateAbstractModel):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    folder = models.ForeignKey(Folder, null=True, blank=True, related_name='files', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)
    size = models.BigIntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
            mime_type, encoding = mimetypes.guess_type(self.file.name)
            self.file_type = mime_type
        super().save(*args, **kwargs)

    def add_user_to_share_list(self, user_id: int) -> None:
        try:
            user = User.objects.get(id=user_id)
            if user not in self.shared_with.all():
                self.shared_with.add(user)
                self.save()
        except User.DoesNotExist:
            raise ValueError("User does not exist")

    def __str__(self):
        return self.name
