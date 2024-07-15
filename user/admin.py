from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import (
    User,
    PushRecord,
    TaskRecord
)

class UserAdmin(BaseUserAdmin):
    ordering = ['username', 'name']
    search_fields = ['email', 'name', 'username',]
    list_display = ['username', 'name', 'email', 'is_active']
    fieldsets = (
        ('Personal info', {'fields': ('name', 'email', 'username',)}),
        ('Secure', {'fields': ('password',), 'classes': ('collapse',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Important dates', {'fields': ('last_login', )}),
        ('Extra', {'fields': ('groups', 'user_permissions',), 'classes':('collapse',)}),
    )
    readonly_fields = ['last_login', ]
    add_fieldsets = (
        ('Add User Information', {
            'classes': ('wide',),
            'fields': (
                'name', 'email', 'username',
            ),
        }),
        ('Secure Password', {
            'classes': ('wide',),
            'fields': (
                'password1', 'password2',
            ),
        }),
        ('Access Permission', {
            'classes': ('wide',),
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
            ),
        }),
    )

class RecordAdmin(admin.ModelAdmin):
    def get_total_time(self, obj):
        time = obj.get_total_time()
        hrs = int(time / 3600)
        mint = int((time % 3600) / 60)
        sec = int((time % 3600) % 60)
        return f'{hrs}:{mint}:{sec}'
    get_total_time.short_description = 'Total Time Taken'

    def task_duration(self, obj):
        return obj.task.duration
    task_duration.short_description = 'Assigned Time'
    
    list_display = ['task', 'user', 'get_total_time', 'task_duration']
    search_fields = ['task', 'user']
    list_filter = ['task', 'user']

# admin.site.register(User)
admin.site.register(User, UserAdmin)
admin.site.register(TaskRecord, RecordAdmin)
admin.site.register(PushRecord)