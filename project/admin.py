from django.contrib import admin
from project.models import (
    Project,
    ProjectFile
)

class ProjectAdmin(admin.ModelAdmin):
    def get_fab_name(self, obj):
        return obj.fabricator.fabName
    get_fab_name.short_description = 'Fabricator'

    def get_team_name(self, obj):
        return obj.team.name
    get_team_name.short_description = 'Team'

    def get_manager_name(self, obj):
        return obj.manager.username
    get_manager_name.short_description = 'Manager'  

    ordering = ['created_at', 'name']
    list_display = [ 'name', 'get_fab_name', 'get_manager_name', 'get_team_name', 'endDate', 'status', 'stage']
    search_fields = ['name', 'description', 'manager__username', 'fabricator__fabName', 'team__name']
    list_filter = ['status', 'stage', 'startDate', 'endDate', 'manager__username', 'fabricator__fabName', 'team__name']
    readonly_fields = ['created_at', 'updated_at',]
    fieldsets = [
        ('Project Information', {'fields': [
            'name', 'description', ]
        }),
        ('Project Members', {'fields': [
            'manager', 'team', 'fabricator', ]
        }),
        ('Project Dates', {'fields': [
            'startDate', 'endDate', ]
        }),
        ('Project Status', {'fields': [
            'status', 'stage'
        ]}),
        ('Files', {'fields':
             ['files', ]
        }),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]
    add_fieldsets = [
        ('Add Project Information', {
            'classes': ('wide',),
            'fields': [ 'name', 'description', ]
        }),
        ('Add Project Members', {
            'classes': ('wide',),
            'fields': ['manager', 'team', 'fabricator', ]
        }),
        ('Add Project Dates', {
            'classes': ('wide',),
            'fields': ['startDate', 'endDate', ]
        }),
        ('Files', {
            'classes': ('wide',),
            'fields': ['files', ]
        }),
    ]



# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectFile)