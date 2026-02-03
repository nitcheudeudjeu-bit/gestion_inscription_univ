from django.contrib import admin
from .models import Faculty, Department, Program, Level

admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Level)
admin.site.register(Program)

