from django.contrib import admin
from task.models import (
    TaskComment,
    Task,
    AssignedList
)


# Register your models here.
admin.site.register(TaskComment)
admin.site.register(AssignedList)
admin.site.register(Task)