from django.contrib import admin
from fabricator.models import Fabricator

class FabricatorAdmin(admin.ModelAdmin):
    ordering = ['name', 'contactPerson',]
    search_fields = ['name', 'contactPerson', 'contactPhone']
    list_display = ['name', 'contactPerson', 'contactPhone', 'contactCountry']
    list_filter = ['contactCountry', 'contactState', 'contactCity', 'contactPerson']    
    fieldsets = (
        ('Fabricator', {
            'fields': ['name']
        }),
        ('Contact Person Info', {
            'fields': ['contactPerson', 'contactPhone', 'contactCountry', 'contactState', 'contactCity']
        }),
        ('Contract Details', {
            'fields': ['contract']
        })
    )

admin.site.register(Fabricator, FabricatorAdmin)