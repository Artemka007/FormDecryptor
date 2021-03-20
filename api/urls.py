from django.urls import path

from . import views

urlpatterns = [
    path('files/download/', views.DownloadFile.as_view(), name="download_files"),
    path('files/download/<int:pk>', views.DownloadFile.as_view(), name="download_files"),
]