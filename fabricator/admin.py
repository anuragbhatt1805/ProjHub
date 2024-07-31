from django.contrib import admin
from fabricator.models import Fabricator, ContactPerson


class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 0

class FabricatorAdmin(admin.ModelAdmin):
    def get_contact_person_count(self, obj):
        return obj.get_contact_person().count()
    get_contact_person_count.short_description = 'No of Contact Persons'

    list_display = ('name', 'country', 'state', 'city', 'zipCode', 'get_contact_person_count')
    list_filter = ('country', 'state', 'city')
    search_fields = ('name', 'country', 'state', 'city', 'zipCode')
    ordering = ['name', 'country', 'state', 'city']
    readonly_fields = ('id',)
    fieldsets = (
        ('Fabricator Information', {
            'fields': ('name', 'country', 'state', 'city', 'zipCode', 'design')
        }),
    )
    inlines = [ContactPersonInline]


admin.site.register(Fabricator, FabricatorAdmin)
admin.site.register(ContactPerson)