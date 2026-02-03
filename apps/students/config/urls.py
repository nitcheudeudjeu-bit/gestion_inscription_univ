from django.urls import path, include

urlpatterns = [
    path("students/", include("apps.students.urls")),
]

