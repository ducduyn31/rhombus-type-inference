from django.urls import path

from webhook.views import MinIOWebhook

urlpatterns = [
    path('minio/', MinIOWebhook.as_view(), name='minio-webhook'),
]
