from django.contrib import admin
from project.models import (
    Project,
    ProjectFile
)

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectFile)