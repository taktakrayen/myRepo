from django.contrib import admin
from .models import Produit,Category,Fournisseur,ProduitNC,Commande

admin.site.register(Produit)
admin.site.register(Category)
admin.site.register(Fournisseur)
admin.site.register(ProduitNC)
admin.site.register(Commande)