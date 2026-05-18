from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('vitrine/', views.vitrine, name='vitrine'),
    path('panier/', views.panier, name='panier'),
    path('ajouter/<int:produit_id>/', views.ajouter_panier, name='ajouter_panier'),
    path('supprimer/<int:ligne_id>/', views.supprimer_panier, name='supprimer_panier'),
    path('valider/', views.valider_commande, name='valider_commande'),
    
    path('checkout/livraison/', views.checkout_livraison, name='checkout_livraison'),
    path('checkout/paiement/', views.checkout_paiement, name='checkout_paiement'),
    path('checkout/confirmation/<int:commande_id>/', views.confirmation_commande, name='confirmation_commande'),

    path('adresses/', views.mes_adresses, name='mes_adresses'),
    path('adresses/supprimer/<int:adresse_id>/', views.supprimer_adresse, name='supprimer_adresse'),
    path('adresses/defaut/<int:adresse_id>/', views.definir_adresse_defaut, name='definir_adresse_defaut'),
]
