from django import forms
from django.contrib.auth.models import User
from .models import Don, Hospital

class DonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = ['groupe_sanguin', 'ville', 'telephone', 'age', 'disponibilite', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Message optionnel...'}),
            'groupe_sanguin': forms.Select(attrs={'class': 'form-select'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Tunis, Sfax...'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 21 234 567'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 18, 'max': 65}),
            'disponibilite': forms.Select(attrs={'class': 'form-select'}),
        }

class LoginDonForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )

class RegisterDonForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (optionnel)'})
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})
    )

class RechercheForm(forms.Form):
    GROUPE_CHOICES = [('', 'Tous les groupes')] + Don.GROUPE_CHOICES
    DISPO_CHOICES = [('', 'Toutes'), ('disponible', 'Disponibles'), ('indisponible', 'Indisponibles'), ('bientot', 'Bientôt disponibles')]

    groupe_sanguin = forms.ChoiceField(
        choices=GROUPE_CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ville = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville...'})
    )
    disponibilite = forms.ChoiceField(
        choices=DISPO_CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['nom', 'ville', 'adresse', 'telephone', 'email', 'capacite']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Hôpital Charles Nicolle'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Tunis, Sfax...'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse complète'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 71 234 567'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (optionnel)'}),
            'capacite': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class DonHospitalForm(forms.Form):
    GROUPE_CHOICES = Don.GROUPE_CHOICES
    DISPONIBILITE_CHOICES = Don.DISPONIBILITE_CHOICES

    nom_donneur = forms.CharField(
        label="Nom du donneur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet du donneur'})
    )
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 21 234 567'})
    )
    age = forms.IntegerField(
        min_value=18, max_value=65,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    groupe_sanguin = forms.ChoiceField(
        choices=GROUPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ville = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Tunis, Sfax...'})
    )
    disponibilite = forms.ChoiceField(
        choices=DISPONIBILITE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Message optionnel...'})
    )
