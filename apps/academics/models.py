from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return f"{self.name} ({self.faculty.name})"


class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="programs")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="programs")

    def __str__(self):
        return f"{self.name} ({self.level.name})"

