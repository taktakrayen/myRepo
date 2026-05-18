from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil_don, name='accueil_don'),
    path('donner/', views.faire_don, name='faire_don'),
    path('mes-dons/', views.mes_dons, name='mes_dons'),
    path('mes-dons/modifier/<int:don_id>/', views.modifier_don, name='modifier_don'),
    path('mes-dons/supprimer/<int:don_id>/', views.supprimer_don, name='supprimer_don'),
    path('login/', views.login_don, name='login_don'),
    path('logout/', views.logout_don, name='logout_don'),
    path('register/', views.register_don, name='register_don'),
    path('hopitaux/', views.liste_hopitaux, name='liste_hopitaux'),
    path('hopitaux/ajouter/', views.ajouter_hopital, name='ajouter_hopital'),
    path('hopitaux/<int:hopital_id>/', views.detail_hopital, name='detail_hopital'),
    path('hopitaux/modifier/<int:hopital_id>/', views.modifier_hopital, name='modifier_hopital'),
    path('hopitaux/supprimer/<int:hopital_id>/', views.supprimer_hopital, name='supprimer_hopital'),
    path('hopitaux/<int:hopital_id>/ajouter-donneur/', views.ajouter_donneur_hopital, name='ajouter_donneur_hopital'),
]
