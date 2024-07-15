from django.contrib import admin
from team.models import Team, Member

class TeamAdmin(admin.ModelAdmin):
    def get_member_count(self, obj):
        return obj.get_members_count()
    
    get_member_count.short_description = 'No of Team Members'
    
    list_display = ('name', 'created_by', 'leader', 'get_member_count')
    list_filter = ('created_by', 'leader')
    search_fields = ('name', 'created_by__username', 'leader__username')
    ordering = ['created_at', 'name']
    readonly_fields = ('created_at', 'created_by')
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'created_by', 'leader')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not request.user.is_staff or not request.user.is_superuser:
            return False
        if not change:
            team = Team.objects.create(
                name=form.cleaned_data['name'],
                created_by=request.user,
                leader=form.cleaned_data['leader']
            )
            team.save()
            return team

class MemberAdmin(admin.ModelAdmin):
    def get_team_name(self, obj):
        return obj.team.name
    get_team_name.short_description = 'Team'

    def get_employee_name(self, obj):
        return obj.employee.name
    get_employee_name.short_description = 'Employee'

    list_display = ('id', 'get_team_name', 'role', 'get_employee_name')
    list_filter = ['team__name', 'role']
    search_fields = ( 'employee', 'team__name')
    ordering = ['id', 'team__name', 'employee__username']
    fieldsets = [
        ('Team Information', {
            'fields': ('team', )
        }),
        ('Member Information', {
            'fields': ('role', 'employee')
        }),
    ]


admin.site.register(Team, TeamAdmin)
admin.site.register(Member, MemberAdmin)
