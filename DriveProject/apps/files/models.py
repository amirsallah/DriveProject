from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='folders', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    folder = models.ForeignKey(Folder, null=True, blank=True, related_name='files', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)

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
