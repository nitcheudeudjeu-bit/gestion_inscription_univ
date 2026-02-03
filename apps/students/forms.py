from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = ['matricule', 'date_naissance', 'telephone', 'level', 'program']

