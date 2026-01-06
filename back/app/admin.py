# admin.py (REMPLACE TON CODE PAR CELUI-CI)

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SalleService, Service, Utilisateur, Salle, Schedule, Course,
    SallePhoto, Avis  # ✅ Ajoute Avis
)

# ==========================================
# INLINE : Afficher les photos dans la page Salle
# ==========================================

class SallePhotoInline(admin.TabularInline):
    """
    Permet de gérer les photos directement depuis la page d'édition de la salle
    """
    model = SallePhoto
    extra = 1  # Affiche 1 ligne vide pour ajouter une nouvelle photo
    fields = ['image_preview', 'image', 'photo_type', 'ordre', 'legende']
    readonly_fields = ['image_preview']  # On ne peut pas éditer l'aperçu
    
    def image_preview(self, obj):
        """
        Affiche un aperçu de l'image dans l'admin
        Si la photo existe, on affiche une miniature de 100x100px
        """
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "Pas d'image"
    
    image_preview.short_description = "Aperçu"  # Nom de la colonne dans l'admin


# ==========================================
# ADMIN PERSONNALISÉ pour Salle
# ==========================================

class SalleAdmin(admin.ModelAdmin):
    """
    Ajoute la gestion des photos dans la page Salle
    """
    inlines = [SallePhotoInline]  # ✅ Inclut les photos dans la page Salle
    
    list_display = ['nom', 'gerant', 'ville', 'wilaya']  # Colonnes affichées
    search_fields = ['nom', 'ville', 'wilaya']  # Barre de recherche
    list_filter = ['wilaya']  # Filtres latéraux


# ==========================================
# ENREGISTRER LES MODÈLES
# ==========================================

admin.site.register(Utilisateur)
admin.site.register(Salle, SalleAdmin)  # ✅ Utilise SalleAdmin personnalisé
admin.site.register(Service)
admin.site.register(SalleService)
admin.site.register(Course)
admin.site.register(Schedule)
admin.site.register(SallePhoto)
admin.site.register(Avis)  # ✅ Enregistre Avis pour tester via l'admin