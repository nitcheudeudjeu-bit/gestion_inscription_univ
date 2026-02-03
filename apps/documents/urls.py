from django.urls import path
from .views import upload_documents

urlpatterns = [
    path("upload/", upload_documents, name="upload_documents"),
]

