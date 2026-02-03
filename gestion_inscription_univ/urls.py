from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('apps.students.urls')),  # Tout ce qui concerne les étudiants
    path("documents/", include("apps.documents.urls")),

]

