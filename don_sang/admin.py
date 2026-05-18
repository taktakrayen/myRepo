from django.contrib import admin
from .models import Don, Hospital

@admin.register(Don)
class DonAdmin(admin.ModelAdmin):
    list_display = ('donneur', 'groupe_sanguin', 'ville', 'age', 'disponibilite', 'date_don')
    list_filter = ('groupe_sanguin', 'disponibilite', 'ville')
    search_fields = ('donneur__username', 'ville', 'telephone')
    ordering = ('-date_don',)
    readonly_fields = ('date_don',)
    list_per_page = 25


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'telephone', 'email', 'capacite', 'date_ajout')
    list_filter = ('ville',)
    search_fields = ('nom', 'ville', 'telephone')
    ordering = ('nom',)
    readonly_fields = ('date_ajout',)
    list_per_page = 25
