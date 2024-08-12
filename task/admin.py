from django.contrib import admin
from .models import Task, TaskComment, AssignedList
from datetime import datetime

class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0
    readonly_fields = ('user', 'created_on')
    fields = ('user', 'data', 'file', 'created_on')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('task',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()

class AssignedListInline(admin.TabularInline):
    model = AssignedList
    extra = 0
    readonly_fields = ('assigned_by', 'approved_by', 'approved_on', 'assigned_on')
    fields = ('assigned_to', 'approved', 'comment', 'assigned_on', 'approved_by', 'approved_on')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('task',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.assigned_by = request.user
        obj.save()

class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskCommentInline, AssignedListInline]

    def get_fab_name(self, obj):
        return obj.fabricator.name
    get_fab_name.short_description = 'Fabricator'

    def get_project_name(self, obj):
        return obj.project.name
    get_project_name.short_description = 'Project'

    def get_user_name(self, obj):
        return obj.user.name  # Assuming user model has get_full_name method
    get_user_name.short_description = 'Current Assignee'

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
    list_filter = ['status', 'priority', 'due_date', 'user__username']
    readonly_fields = ['created_on', 'fabricator', 'get_child_tasks_display']
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
            'classes': ('wide',),
            'fields': [
                'parent', 'get_child_tasks_display'
            ]
        }),
        ('Important Dates', {
            'classes': ('shrink',),
            'fields': [
                'due_date',
            ]
        }),
        ('Attachment', {
            'fields': ['attachment'],
        }),
        ('User', {
            'classes': ('wide',),
            'fields': ['user'],
        }),
        ('Timestamps', {'fields': ['created_on']}),
    ]

    def save_model(self, request, obj, form, change):
        if change:
            if 'project' in form.changed_data and obj.project:
                obj.fabricator = obj.project.fabricator
            if 'user' in form.changed_data and obj.user:
                assigned_list = AssignedList.objects.create(
                    task=obj,
                    assigned_by=request.user,
                    assigned_to=obj.user,
                    approved_by=request.user,
                    approved_on=datetime.now(),
                    approved=True,
                    comment='User reassigned in admin interface'
                )
                assigned_list.save()
        else:
            obj.fabricator = obj.project.fabricator
        obj.save()

        if not change:
            assigned_list = AssignedList.objects.create(
                task=obj,
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
        return obj.user.name  # Assuming user model has get_full_name method
    get_user_name.short_description = 'User'

    list_display = ['get_task_name', 'get_user_name', 'data']
    search_fields = ['task__name', 'user__username', 'data']
    list_filter = ['task__name', 'user__username']
    ordering = ['task', 'user']
    readonly_fields = ['user']
    fieldsets = (
        ('Task and Comment', {
            'fields': ['task']
        }),
        ('Comment', {
            'fields': ['data', 'file']
        }),
        ('User', {
            'fields': ['user']
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskComment, CommentAdmin)
admin.site.register(AssignedList)
