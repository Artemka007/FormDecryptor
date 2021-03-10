from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="decryptor_index"),
    path('upload/', views.upload, name='decryptor_upload'),
    path('upload/ui/', views.upload_files_controller, name='decryptor_blank_upload'),
    path('upload/delete/<int:pk>', views.delete_upload_files_controller, name='decryptor_blank_upload_delete'),
]