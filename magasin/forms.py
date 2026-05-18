from django.forms import ModelForm
from django import forms
from .models import Produit, Fournisseur

class ProduitForm(ModelForm):
    class Meta:
        model = Produit
        fields = "__all__"

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)