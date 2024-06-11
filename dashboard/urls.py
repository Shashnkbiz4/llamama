from django.urls import path
from . import views
app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='index'),
    path('upload/', views.upload, name='upload'),
    path('multiple-upload/', views.file_upload, name='file_upload'),
    # path('multi-upload/', views.multiple_upload, name='multiupload'),
    # path('multiple-upload/', views.multiple_upload, name='multiple_upload'),
    # path('process_pdf/', views.process_pdf, name='process_pdf'),
    # path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
]