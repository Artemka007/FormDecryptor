from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="decryptor_index"),
    path('test/download/', views.test_download_excel_file, name='test_download_excel_file'),
    path('download/<int:pk>', views.download_excel_file, name='download_excel_file'),
    path('upload/ui/', views.upload_files_controller, name='decryptor_blank_upload'),
    path('upload/createExcel/<int:pk>', views.send_file, name='createExcel'),
    path('upload/delete/<int:pk>', views.delete_upload_files_controller, name='decryptor_blank_upload_delete'),
]