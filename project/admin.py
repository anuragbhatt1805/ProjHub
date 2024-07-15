from django.contrib import admin
from project.models import (
    Project,
    ProjectFile
)

class ProjectAdmin(admin.ModelAdmin):
    def get_fab_name(self, obj):
        return obj.fabricator.name
    get_fab_name.short_description = 'Fabricator'

    def get_team_name(self, obj):
        if obj.team:
            return obj.team.name
        return "Team Not Selected"
    get_team_name.short_description = 'Team'

    def get_manager_name(self, obj):
        return obj.manager.username
    get_manager_name.short_description = 'Manager'  

    ordering = ['created_at', 'name']
    list_display = [ 'name', 'get_fab_name', 'get_manager_name', 'get_team_name', 'endDate', 'status', 'stage']
    search_fields = ['name', 'description', 'manager__name', 'fabricator__name', 'team__name']
    list_filter = ['status', 'stage', 'startDate', 'endDate', 'manager__name', 'fabricator__name', 'team__name']
    readonly_fields = ['created_at', 'updated_at',]
    fieldsets = [
        ('Project Information', {'fields': [
            'name', 'description', ],
            'classes': ('wide',),
        }),
        ('Project Members', {'fields': [
            'manager', 'team', 'fabricator', ],
            'classes': ('wide',),
        }),
        ('Project Dates', {'fields': [
            'startDate', 'endDate', ],
            'classes': ('shrink',),
        }),
        ('Project Status', {'fields': [
            'status', 'stage'],
            'classes': ('wide',),
        }),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]

class ProjectFileAdmin(admin.ModelAdmin):
    ordering = ['id', 'project']
    search_fields = ['detail', ]
    list_filter = ['project', ]
    fieldsets = [
        ('Project', {
            'fields':['project',],
        }),
        ('Files', {
            'fields':['file', ],
        }), ( 'Caption', {
            'fields':['detail', ],
        })
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectFile, ProjectFileAdmin)