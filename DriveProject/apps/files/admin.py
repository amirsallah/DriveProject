from django.contrib import admin

from .models import Folder, File


class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'owner')


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'folder', 'owner')


admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)
