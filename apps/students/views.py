# apps/students/views.py
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from apps.students.models import Student
from apps.academics.models import Level, Program
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# --- Inscription ---
def student_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        matricule = request.POST.get("matricule")
        date_naissance = request.POST.get("date_naissance")
        telephone = request.POST.get("telephone")
        level_id = request.POST.get("level")
        program_id = request.POST.get("program")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return redirect("student_register")

        if Student.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect("student_register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        level = Level.objects.get(id=level_id)
        program = Program.objects.get(id=program_id)

        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            matricule=matricule,
            date_naissance=date_naissance,
            telephone=telephone,
            level=level,
            program=program
        )

        return redirect("registration_success")

    return render(
        request,
        "students/register.html",
        {
            "levels": Level.objects.all(),
            "programs": Program.objects.all()
        }
    )


# --- Succès ---
def registration_success(request):
    return render(request, "students/registration_success.html")


# --- Login ---
def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("student_dashboard")

        messages.error(request, "Identifiants incorrects")
        return redirect("student_login")

    return render(request, "students/login.html")


# --- Logout ---
def student_logout(request):
    logout(request)
    return redirect("student_login")


# --- Dashboard ---
# apps/students/views.py

from django.shortcuts import render, get_object_or_404
from .models import Student

def student_dashboard(request):
    student = get_object_or_404(Student, email=request.user.email)

    return render(request, "students/dashboard.html", {
        "student": student
    })

# --- Modifier profil ---
@login_required
def edit_student_profile(request):
    student = Student.objects.get(email=request.user.email)

    if request.method == "POST":
        student.telephone = request.POST.get("telephone")
        student.date_naissance = request.POST.get("date_naissance")
        student.level_id = request.POST.get("level")
        student.program_id = request.POST.get("program")
        student.save()

        messages.success(request, "Profil mis à jour avec succès")
        return redirect("student_dashboard")

    return render(request, "students/edit_profile.html", {
        "student": student,
        "levels": Level.objects.all(),
        "programs": Program.objects.all()
    })
    from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from datetime import date
from django.contrib.auth.decorators import login_required
## apps/students/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os
from .models import Student

@login_required
def student_confirmation_pdf(request):
    # Récupération du Student via l'email de l'utilisateur connecté
    student = get_object_or_404(Student, email=request.user.email)

    # Création de la réponse PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="attestation_{student.matricule}.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # --- Ajouter le logo ---
    logo_path = os.path.join('apps', 'students', 'static', 'images', 'university_logo.png')
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.drawImage(logo, x=50, y=height-120, width=100, height=100)
    
    # --- Titre ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-50, "Université de Yaoundé I")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height-70, "Attestation d’inscription")

    # --- Informations de l'étudiant ---
    c.setFont("Helvetica", 12)
    y = height - 150
    c.drawString(50, y, f"Nom et prénom : {student.first_name} {student.last_name}")
    y -= 20
    c.drawString(50, y, f"Matricule : {student.matricule}")
    y -= 20
    c.drawString(50, y, f"Email : {student.email}")
    y -= 20
    c.drawString(50, y, f"Téléphone : {student.telephone}")
    y -= 20
    c.drawString(50, y, f"Niveau : {student.level}")
    y -= 20
    c.drawString(50, y, f"Programme : {student.program}")

    # --- Statut des documents ---
    y -= 40
    if student.documents:
        if student.documents.is_validated:
            c.drawString(50, y, "Statut des documents : ✅ Validés")
        elif student.documents.is_refused:
            c.drawString(50, y, "Statut des documents : ❌ Refusés")
            if student.documents.admin_comment:
                y -= 20
                c.drawString(50, y, f"Motif : {student.documents.admin_comment}")
        else:
            c.drawString(50, y, "Statut des documents : ⏳ En attente")
    else:
        c.drawString(50, y, "Statut des documents : Aucun document soumis")

    # --- Finalisation ---
    c.showPage()
    c.save()
    return response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Payment
import uuid

@login_required
def student_payment(request):
    student = get_object_or_404(Student, email=request.user.email)

    if request.method == "POST":
        payment = Payment.objects.create(
            student=student,
            amount=50000,  # Droits universitaires
            method="Mobile Money",
            status="SUCCESS",  # simulation
            transaction_id=str(uuid.uuid4())
        )
        return redirect('payment_success')

    return render(request, 'students/payment.html', {
        'student': student,
        'amount': 50000
    })


@login_required
def payment_success(request):
    return render(request, 'students/payment_success.html')

