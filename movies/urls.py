from django.urls import path
from . import views, controller

urlpatterns = [
    path('', views.page_inicial, name='index'),

    path('api/upload/', controller.upload_arquivo, name='api_upload_arquivo'),
    path('api/delete/<int:id>', controller.delete_arquivo_reports, name='api_delet_upload'),
]
