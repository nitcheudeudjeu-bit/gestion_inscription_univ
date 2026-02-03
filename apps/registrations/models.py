#from django.db import models

# Create your models here.
from django.db import models
from apps.students.models import Student
from apps.academics.models import Program, Level


class Registration(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Validée'),
        ('REJECTED', 'Rejetée'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    academic_year = models.CharField(max_length=9)  # ex: 2025-2026
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.matricule} - {self.academic_year}"

