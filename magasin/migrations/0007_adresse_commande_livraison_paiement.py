import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0006_remove_commande_produits_remove_commande_totalcde_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Créer le modèle Adresse
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_complet', models.CharField(max_length=100, verbose_name='Nom complet')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('adresse', models.TextField(verbose_name='Adresse')),
                ('ville', models.CharField(max_length=100, verbose_name='Ville')),
                ('code_postal', models.CharField(max_length=10, verbose_name='Code postal')),
                ('par_defaut', models.BooleanField(default=False, verbose_name='Adresse par défaut')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='adresses',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={'ordering': ['-par_defaut', '-created_at']},
        ),
        # Ajouter statut à Commande
        migrations.AddField(
            model_name='commande',
            name='statut',
            field=models.CharField(
                choices=[
                    ('panier', 'En cours'),
                    ('en_attente', 'En attente de paiement'),
                    ('payee', 'Payée'),
                    ('en_livraison', 'En cours de livraison'),
                    ('livree', 'Livrée'),
                ],
                default='panier',
                max_length=20
            ),
        ),
        # Ajouter adresse_livraison à Commande
        migrations.AddField(
            model_name='commande',
            name='adresse_livraison',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='magasin.adresse'
            ),
        ),
        # Ajouter frais_livraison
        migrations.AddField(
            model_name='commande',
            name='frais_livraison',
            field=models.DecimalField(decimal_places=3, default=7.0, max_digits=8),
        ),
        # Ajouter mode_paiement
        migrations.AddField(
            model_name='commande',
            name='mode_paiement',
            field=models.CharField(
                blank=True, null=True,
                choices=[
                    ('carte', 'Carte bancaire'),
                    ('especes', 'Paiement à la livraison'),
                    ('virement', 'Virement bancaire'),
                ],
                max_length=20
            ),
        ),
        # Ajouter paiement_confirme
        migrations.AddField(
            model_name='commande',
            name='paiement_confirme',
            field=models.BooleanField(default=False),
        ),
        # Ajouter date_paiement
        migrations.AddField(
            model_name='commande',
            name='date_paiement',
            field=models.DateTimeField(blank=True, null=True),
        ),
        # Ajouter numero_suivi
        migrations.AddField(
            model_name='commande',
            name='numero_suivi',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
