# apps/students/models.py

from django.db import models
from apps.academics.models import Level, Program


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    matricule = models.CharField(max_length=50, unique=True)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)

    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    is_documents_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
from django.db import models
from django.utils import timezone

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('PENDING', 'En attente'),
        ('SUCCESS', 'Payé'),
        ('FAILED', 'Échoué'),
    )

    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.PositiveIntegerField()
    method = models.CharField(
        max_length=50,
        default="Mobile Money"
    )
    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default='PENDING'
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.matricule} - {self.amount} FCFA"

