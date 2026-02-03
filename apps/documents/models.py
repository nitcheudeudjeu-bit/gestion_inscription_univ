from django.db import models
from apps.students.models import Student

class Document(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    acte_naissance = models.FileField(upload_to="actes/", blank=True, null=True)
    diplome = models.FileField(upload_to="diplomes/", blank=True, null=True)

    is_validated = models.BooleanField(default=False)
    is_refused = models.BooleanField(default=False)

    admin_comment = models.TextField(
        blank=True,
        null=True,
        help_text="Raison du refus (visible par l'étudiant)"
    )

    validated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documents - {self.student.matricule}"

