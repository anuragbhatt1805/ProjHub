from typing import Any
from django.contrib import admin
from .models import Task, TaskComment, AssignedList
from datetime import datetime

# from django import forms

# class TaskAdminForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         exclude = []

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         instance = kwargs.get('instance')
#         # Add a button to add child task
#         self.fields['add_child_task'] = forms.ModelChoiceField(
#             queryset=Task.objects.exclude(pk=instance.pk) if instance and instance.pk else Task.objects.none(),
#             required=True,
#             widget=forms.Select(attrs={'onchange': 'this.form.submit();'}),
#             label='Add Child Task',
#             empty_label='---------'
#         )



class TaskAdmin(admin.ModelAdmin):

    # form = TaskAdminForm

    def get_fab_name(self, obj):
        return obj.fabricator.name
    get_fab_name.short_description = 'Fabricator'

    def get_project_name(self, obj):
        return obj.project.name
    get_project_name.short_description = 'Project'

    def get_user_name(self, obj):
        return obj.user.name
    get_user_name.short_description = 'Current Assigne'

    def get_child_tasks_display(self, obj):
        child_tasks = obj.get_child_tasks()
        if child_tasks.exists():
            return ', '.join([task.name for task in child_tasks])
        else:
            return '-'
    get_child_tasks_display.short_description = 'Child Tasks'


    ordering = ['fabricator', 'project']
    list_display = ['name', 'get_fab_name', 'get_project_name', 'status', 'priority', 'get_user_name', 'get_child_tasks_display']
    search_fields = ['fabricator__name', 'project__name', 'name', 'description']
    list_filter = ['status', 'priority', 'due_date', 'user__name']
    readonly_fields = ['created_on', 'fabricator', 'get_child_tasks_display',]
    fieldsets = [
        ('Project Information', {'fields': [
            'project', 'fabricator'],
            'classes': ('wide',),
        }),
        ('Task Information', {
            'classes': ('wide',),
            'fields': [
                'name', 'description', 'status', 'priority',
                'duration',
            ]
        }),
        ('Task Tree', {
            'classes':('wide',),
            'fields': [
                'parent', 'get_child_tasks_display'
            ]
        }),
        ('Important Dates', {
            'classes':('shrink',),
            'fields': [
                'due_date',
            ]
        }),
        ('Attachment', {
            'fields':['attachment',],
        }),
        ('User', {
            'classes':('wide',),
            'fields':['user',],
        }),
        ('Timestamps', {'fields': ['created_on']}),
    ]

    def save_model(self, request, obj, form, change):
        if change:
            if 'project' in form.changed_data and obj.project:
                obj.fabricator = obj.project.fabricator
            if 'user' in form.changed_data and obj.user:
                assigned_list = AssignedList.objects.create(
                    assigned_by=request.user,
                    assigned_to=obj.user,
                    approved_by=request.user,
                    approved_on=datetime.now(),
                    approved=True,
                    comment='First User Assigned To Task'
                )
                assigned_list.save()
        else:
            obj.fabricator = obj.project.fabricator

        obj.save()

        if not change:
            assigned_list = AssignedList.objects.create(
                assigned_by=request.user,
                assigned_to=obj.user,
                approved_by=request.user,
                approved_on=datetime.now(),
                approved=True,
                comment='First User Assigned To Task'
            )
            assigned_list.save()
        
        super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):

    def get_task_name(self, obj):
        return obj.task.name
    get_task_name.short_description = 'Task'

    def get_user_name(self, obj):
        return obj.user.name
    get_user_name.short_description = 'User'

    list_display = ['get_task_name', 'get_user_name', 'data']
    search_fields = ['task__name', 'user__name', 'data']
    list_filter = ['task__name', 'user__name']
    ordering = ['task', 'user']
    readonly_fields = ['user', ]
    fieldsets = (
        ('Task and Comment', {
            'fields': ['task', ]
        }),
        ('Comment', {
            'fields': ['data', 'file',]
        }),
        ('User', {
            'fields': ['user',]
        }),
    )

    def save_model(self, request: Any, obj: Any, form: Any, change: Any):
        comment = TaskComment.objects.create(
            task=obj.task,
            user=request.user,
            data=obj.data,
            file=obj.file
        )
        comment.save()
        return comment

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskComment, CommentAdmin)
admin.site.register(AssignedList)
