from django.contrib import admin
from .models import Project, ProjectFile

class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 0
    fields = ('file', 'detail')

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectFileInline]

    def get_fab_name(self, obj):
        return obj.fabricator.name
    get_fab_name.short_description = 'Fabricator'

    def get_team_name(self, obj):
        if obj.team:
            return obj.team.name
        return "Team Not Selected"
    get_team_name.short_description = 'Team'

    def get_manager_name(self, obj):
        return obj.manager.name
    get_manager_name.short_description = 'Manager'

    ordering = ['created_at', 'name']
    list_display = ['name', 'get_fab_name', 'get_manager_name', 'get_team_name', 'endDate', 'status', 'stage']
    search_fields = ['name', 'description', 'manager__username', 'fabricator__name', 'team__name']
    list_filter = ['status', 'stage', 'startDate', 'endDate', 'manager__username', 'fabricator__name', 'team__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Project Information', {'fields': [
            'name', 'description', ],
            'classes': ('wide',),
        }),
        ('Project Members', {'fields': [
            'manager', 'team', 'fabricator', ],
            'classes': ('wide',),
        }),
        ('Project Details', {'fields': [
            'tool', 'connectionDesign', 'miscDesign'],
            'classes': ('wide',),
        }),
        ('Project Dates', {'fields': [
            'startDate', 'endDate', 'duration'],
            'classes': ('shrink',),
        }),
        ('Project Status', {'fields': [
            'status', 'stage'],
            'classes': ('wide',),
        }),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.manager = request.user
        obj.save()
        super().save_model(request, obj, form, change)

class ProjectFileAdmin(admin.ModelAdmin):
    ordering = ['id', 'project']
    search_fields = ['detail']
    list_filter = ['project']
    fieldsets = [
        ('Project', {
            'fields': ['project'],
        }),
        ('Files', {
            'fields': ['file'],
        }),
        ('Caption', {
            'fields': ['detail'],
        }),
    ]

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectFile, ProjectFileAdmin)
