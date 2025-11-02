from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_inicial, name='index'),

    path('api/upload/', views.upload_arquivo, name='api_upload_arquivo'),
]
