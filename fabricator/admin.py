from django.contrib import admin
from fabricator.models import Fabricator

class FabricatorAdmin(admin.ModelAdmin):
    ordering = ['fabName', 'contactPerson',]
    search_fields = ['fabName', 'contactPerson', 'contactPhone']
    list_display = ['fabName', 'contactPerson', 'contactPhone', 'contactCountry']
    list_filter = ['contactCountry', 'contactState', 'contactCity', 'contactPerson']    
    fieldsets = (
        ('Fabricator', {
            'fields': ['fabName']
        }),
        ('Contact Person Info', {
            'fields': ['contactPerson', 'contactPhone', 'contactCountry', 'contactState', 'contactCity']
        }),
        ('Contract Details', {
            'fields': ['contract']
        })
    )

admin.site.register(Fabricator, FabricatorAdmin)