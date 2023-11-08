from django.urls import path
from . import views

app_name = 'csvmerge'  # Define app name to avoid naming conflicts

urlpatterns = [
    path('', views.upload_view, name='upload_files'),  # URL for uploading files
    path('download_file/', views.download_view, name='download_file'),  # URL for downloading merged file
]
