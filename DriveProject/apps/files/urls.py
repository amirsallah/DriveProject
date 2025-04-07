from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.File.as_view(), name='upload_file'),
    path('list/<int:pk>/', views.File.as_view(), name='list_files'),
    path('detail/<int:pk>/', views.FileDetail.as_view(), name='detail_file'),
    path('download/', views.FileDownload.as_view(), name='download_file'),
    path('delete/<int:pk>/', views.FileDetail.as_view(), name='delete_file'),
    path('share/<int:pk>/', views.FileShare.as_view(), name='share_file'),
    path('unshare/<int:pk>/', views.FileUnshare.as_view(), name='unshare_file'),

    path('folder/', views.Folder.as_view(), name='create_folder'),
    path('folder/<int:pk>/', views.FolderDetail.as_view(), name='folder_detail'),
]
