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

# admin.site.register(User)
admin.site.register(User, UserAdmin)
admin.site.register(TaskRecord)
admin.site.register(PushRecord)