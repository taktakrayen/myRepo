from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    nom = models.CharField(max_length=200)
    ville = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    capacite = models.PositiveIntegerField(help_text="Capacité de stockage de poches de sang", default=0)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']
        verbose_name = 'Hôpital'
        verbose_name_plural = 'Hôpitaux'

    def __str__(self):
        return f"{self.nom} — {self.ville}"

class Don(models.Model):
    GROUPE_CHOICES = [
        ('A+','A+'), ('A-','A-'), ('B+','B+'), ('B-','B-'),
        ('AB+','AB+'), ('AB-','AB-'), ('O+','O+'), ('O-','O-'),
    ]
    DISPONIBILITE_CHOICES = [
        ('disponible', 'Disponible'),
        ('indisponible', 'Indisponible'),
        ('bientot', 'Disponible bientôt'),
    ]

    donneur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dons')
    hopital = models.ForeignKey('Hospital', on_delete=models.SET_NULL, null=True, blank=True, related_name='dons', verbose_name='Hôpital')
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPE_CHOICES)
    date_don = models.DateField(auto_now_add=True)
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=18, help_text="Âge du donneur")
    disponibilite = models.CharField(max_length=20, choices=DISPONIBILITE_CHOICES, default='disponible')
    message = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_don']
        verbose_name = 'Don de sang'
        verbose_name_plural = 'Dons de sang'

    def __str__(self):
        return f"{self.donneur.username} — {self.groupe_sanguin} — {self.date_don}"
