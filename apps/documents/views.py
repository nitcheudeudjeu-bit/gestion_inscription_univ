from django.shortcuts import render, redirect
from django.contrib import messages
from apps.students.models import Student
from .models import Document
from django.contrib.auth.decorators import login_required

@login_required
def upload_documents(request):
    student = Student.objects.get(email=request.user.email)

    document, created = Document.objects.get_or_create(student=student)

    if document.is_validated:
        messages.error(request, "Documents déjà validés. Modification interdite.")
        return redirect("student_dashboard")

    if request.method == "POST":
        document.photo = request.FILES.get("photo")
        document.acte_naissance = request.FILES.get("acte_naissance")
        document.diplome = request.FILES.get("diplome")
        document.save()

        messages.success(request, "Documents envoyés avec succès")
        return redirect("student_dashboard")

    return render(request, "documents/upload_documents.html")

