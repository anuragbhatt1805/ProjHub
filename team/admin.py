from django.contrib import admin
from django.db.models import Count
from team.models import (
    Team,
    Member
)

class MemberCountFilter(admin.SimpleListFilter):
    title = 'Member Count'
    parameter_name = 'member_count'

    def lookups(self, request, model_admin):
        return [
            ('0', '0 Members'),
            ('1-5', '1-5 Members'),
            ('6-10', '6-10 Members'),
            ('11+', '11 or more Members'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(member_count=Count('members')).filter(member_count=0)
        elif self.value() == '1-5':
            return queryset.annotate(member_count=Count('members')).filter(member_count__range=(1, 5))
        elif self.value() == '6-10':
            return queryset.annotate(member_count=Count('members')).filter(member_count__range=(6, 10))
        elif self.value() == '11+':
            return queryset.annotate(member_count=Count('members')).filter(member_count__gt=10)
        else:
            return queryset

class TeamAdmin(admin.ModelAdmin):
    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'No of Team Members'

    list_display = ('name', 'created_by', 'leader', 'get_member_count')
    list_filter = (MemberCountFilter, 'created_by', 'leader')
    search_fields = ('name', 'created_by', 'leader')
    ordering = ['created_at', 'name']
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'created_by', 'leader')
        }),
        ('Members', {
            'fields': ('members',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        })
    )


admin.site.register(Team, TeamAdmin)
admin.site.register(Member)