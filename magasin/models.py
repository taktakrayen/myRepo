from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Category(models.Model):
    TYPE_CHOICES = [
        ('Al', 'Alimentaire'), ('Mb', 'Meuble'),
        ('Sn', 'Sanitaire'), ('Vs', 'Vaisselle'),
        ('Vt', 'Vêtement'), ('Jx', 'Jouets'),
        ('Lg', 'Linge de Maison'), ('Bj', 'Bijoux'), ('Dc', 'Décor')
    ]
    name = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Al')

    def __str__(self):
        return self.get_name_display()


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField(max_length=254)
    telephone = models.CharField(max_length=8)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    TYPE_CHOICES = [('em', 'emballé'), ('fr', 'Frais'), ('cs', 'Conserve')]

    libelle = models.CharField(max_length=100)
    description = models.TextField(default='non définie')
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='em')
    img = models.ImageField(upload_to='produits/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.libelle} ({self.type}) - {self.prix} DT"


class ProduitNC(Produit):
    Duree_garantie = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.libelle} - Garantie: {self.Duree_garantie}"


class Adresse(models.Model):
    """Adresse de livraison enregistrée pour un utilisateur"""
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adresses')
    nom_complet = models.CharField(max_length=100, verbose_name="Nom complet")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    adresse = models.TextField(verbose_name="Adresse")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    code_postal = models.CharField(max_length=10, verbose_name="Code postal")
    par_defaut = models.BooleanField(default=False, verbose_name="Adresse par défaut")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_complet} — {self.adresse}, {self.ville}"

    class Meta:
        ordering = ['-par_defaut', '-created_at']


class Commande(models.Model):
    STATUT_CHOICES = [
        ('panier', 'En cours'),
        ('en_attente', 'En attente de paiement'),
        ('payee', 'Payée'),
        ('en_livraison', 'En cours de livraison'),
        ('livree', 'Livrée'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dateCde = models.DateField(default=date.today)
    validee = models.BooleanField(default=False)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='panier')

    # Livraison
    adresse_livraison = models.ForeignKey(
        Adresse, on_delete=models.SET_NULL, null=True, blank=True
    )
    frais_livraison = models.DecimalField(max_digits=8, decimal_places=3, default=7.000)

    # Paiement
    PAIEMENT_CHOICES = [
        ('carte', 'Carte bancaire'),
        ('especes', 'Paiement à la livraison'),
        ('virement', 'Virement bancaire'),
    ]
    mode_paiement = models.CharField(
        max_length=20, choices=PAIEMENT_CHOICES, null=True, blank=True
    )
    paiement_confirme = models.BooleanField(default=False)
    date_paiement = models.DateTimeField(null=True, blank=True)

    # Numéro de suivi simulé
    numero_suivi = models.CharField(max_length=20, null=True, blank=True)

    def total_produits(self):
        return sum(ligne.sous_total() for ligne in self.lignecommande_set.all())

    def total(self):
        return self.total_produits() + self.frais_livraison

    def __str__(self):
        return f"Commande {self.id} - {self.dateCde} [{self.get_statut_display()}]"


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)

    def sous_total(self):
        return self.produit.prix * self.quantite

    def __str__(self):
        return f"{self.quantite} x {self.produit.libelle}"
