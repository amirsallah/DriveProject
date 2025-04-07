from django.urls import path

# Import views from the files app
from . import views

urlpatterns = [
    # Define URL patterns for the files app
    path('upload/', views.File.as_view(), name='upload_file'),
    path('list/', views.File.as_view(), name='list_files'),
    path('detail/<int:pk>/', views.FileDetail.as_view(), name='detail_file'),
    path('download/', views.FileDownload.as_view(), name='download_file'),
]