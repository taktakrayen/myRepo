import random
import string
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Min, Max
from .models import Produit, Commande, LigneCommande, Adresse, Category
from .forms import ProduitForm


def _nb_panier(user):
    if not user.is_authenticated:
        return 0
    try:
        c = Commande.objects.get(utilisateur=user, validee=False)
        return c.lignecommande_set.count()
    except Commande.DoesNotExist:
        return 0


def _gen_suivi():
    return 'MG' + ''.join(random.choices(string.digits, k=8))


# User registration view
def register_view(request):
    if request.user.is_authenticated:
        return redirect('vitrine')
    error = None
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if not username or not password1:
            error = "Veuillez remplir tous les champs obligatoires."
        elif password1 != password2:
            error = "Les mots de passe ne correspondent pas."
        elif len(password1) < 6:
            error = "Le mot de passe doit contenir au moins 6 caractères."
        elif User.objects.filter(username=username).exists():
            error = "Ce nom d'utilisateur est déjà pris."
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f"Bienvenue {username} ! Compte créé avec succès.")
            return redirect('vitrine')
    return render(request, 'magasin/register.html', {'error': error})


# User login and logout views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('vitrine')
    error = None
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('vitrine')
        else:
            error = "Identifiants incorrects. Veuillez réessayer."
    return render(request, 'magasin/login.html', {'error': error})


def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('vitrine')


# Product showcase with filters and sorting
def vitrine(request):
    produits = Produit.objects.all()
    categories = Category.objects.all()

    # Filtre par catégorie
    cat_id = request.GET.get('categorie')
    cat_active = None
    if cat_id:
        produits = produits.filter(category__id=cat_id)
        try:
            cat_active = Category.objects.get(id=cat_id)
        except Category.DoesNotExist:
            pass

    # Filtre par prix
    prix_min = request.GET.get('prix_min', '')
    prix_max = request.GET.get('prix_max', '')
    if prix_min:
        try:
            produits = produits.filter(prix__gte=float(prix_min))
        except ValueError:
            pass
    if prix_max:
        try:
            produits = produits.filter(prix__lte=float(prix_max))
        except ValueError:
            pass

    # Tri
    tri = request.GET.get('tri', '')
    if tri == 'prix_asc':
        produits = produits.order_by('prix')
    elif tri == 'prix_desc':
        produits = produits.order_by('-prix')
    elif tri == 'nom':
        produits = produits.order_by('libelle')

    # Stats prix pour le slider
    stats = Produit.objects.aggregate(pmin=Min('prix'), pmax=Max('prix'))
    global_min = float(stats['pmin'] or 0)
    global_max = float(stats['pmax'] or 1000)

    # Compteur par catégorie
    categories_avec_count = []
    for cat in categories:
        count = Produit.objects.filter(category=cat).count()
        categories_avec_count.append({'cat': cat, 'count': count})

    return render(request, 'magasin/vitrine.html', {
        'list': produits,
        'nb_panier': _nb_panier(request.user),
        'categories': categories_avec_count,
        'cat_active': cat_active,
        'prix_min': prix_min,
        'prix_max': prix_max,
        'tri': tri,
        'global_min': global_min,
        'global_max': global_max,
        'total_produits': produits.count(),
    })


# Shopping cart functions
@login_required(login_url='/magasin/login/')
def ajouter_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    commande, _ = Commande.objects.get_or_create(utilisateur=request.user, validee=False)
    ligne, created = LigneCommande.objects.get_or_create(commande=commande, produit=produit)
    if not created:
        ligne.quantite += 1
        ligne.save()
    messages.success(request, f"« {produit.libelle} » ajouté au panier !")
    # Revenir à la même page
    next_url = request.META.get('HTTP_REFERER', '/magasin/vitrine/')
    return redirect(next_url)


@login_required(login_url='/magasin/login/')
def supprimer_panier(request, ligne_id):
    ligne = get_object_or_404(LigneCommande, id=ligne_id)
    ligne.delete()
    messages.info(request, "Article supprimé du panier.")
    return redirect('panier')


@login_required(login_url='/magasin/login/')
def panier(request):
    try:
        commande = Commande.objects.get(utilisateur=request.user, validee=False)
        lignes = commande.lignecommande_set.all()
    except Commande.DoesNotExist:
        commande = None
        lignes = []
    return render(request, 'magasin/panier.html', {
        'commande': commande,
        'lignes': lignes,
        'nb_panier': _nb_panier(request.user),
    })


# Checkout step 1: Delivery address
@login_required(login_url='/magasin/login/')
def checkout_livraison(request):
    try:
        commande = Commande.objects.get(utilisateur=request.user, validee=False)
    except Commande.DoesNotExist:
        return redirect('vitrine')

    if not commande.lignecommande_set.exists():
        messages.warning(request, "Votre panier est vide.")
        return redirect('panier')

    adresses = Adresse.objects.filter(utilisateur=request.user)

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'choisir':
            adresse_id = request.POST.get('adresse_id')
            adresse = get_object_or_404(Adresse, id=adresse_id, utilisateur=request.user)
            commande.adresse_livraison = adresse
            commande.save()
            return redirect('checkout_paiement')

        elif action == 'nouvelle':
            nom = request.POST.get('nom_complet', '').strip()
            tel = request.POST.get('telephone', '').strip()
            adr = request.POST.get('adresse', '').strip()
            ville = request.POST.get('ville', '').strip()
            cp = request.POST.get('code_postal', '').strip()
            sauvegarder = request.POST.get('sauvegarder') == 'on'

            if not all([nom, tel, adr, ville, cp]):
                messages.error(request, "Veuillez remplir tous les champs de l'adresse.")
                return render(request, 'magasin/checkout_livraison.html', {
                    'commande': commande, 'adresses': adresses,
                    'nb_panier': _nb_panier(request.user),
                })

            if sauvegarder:
                par_defaut = not adresses.exists()
                adresse = Adresse.objects.create(
                    utilisateur=request.user,
                    nom_complet=nom, telephone=tel,
                    adresse=adr, ville=ville,
                    code_postal=cp, par_defaut=par_defaut
                )
                messages.success(request, "Adresse enregistrée dans votre compte.")
            else:
                adresse = Adresse(
                    utilisateur=request.user,
                    nom_complet=nom, telephone=tel,
                    adresse=adr, ville=ville, code_postal=cp
                )
                adresse.save()

            commande.adresse_livraison = adresse
            commande.save()
            return redirect('checkout_paiement')

    return render(request, 'magasin/checkout_livraison.html', {
        'commande': commande,
        'adresses': adresses,
        'nb_panier': _nb_panier(request.user),
    })


# Checkout step 2: Payment method
@login_required(login_url='/magasin/login/')
def checkout_paiement(request):
    try:
        commande = Commande.objects.get(utilisateur=request.user, validee=False)
    except Commande.DoesNotExist:
        return redirect('vitrine')

    if not commande.adresse_livraison:
        return redirect('checkout_livraison')

    error = None

    if request.method == "POST":
        mode = request.POST.get('mode_paiement')

        if mode == 'carte':
            num = request.POST.get('carte_numero', '').replace(' ', '')
            exp = request.POST.get('carte_expiry', '')
            cvv = request.POST.get('carte_cvv', '')
            nom = request.POST.get('carte_nom', '').strip()

            if len(num) < 16 or not num.isdigit():
                error = "Numéro de carte invalide (16 chiffres requis)."
            elif not exp or len(exp) < 5:
                error = "Date d'expiration invalide."
            elif len(cvv) < 3:
                error = "CVV invalide."
            elif not nom:
                error = "Veuillez entrer le nom sur la carte."
            else:
                commande.mode_paiement = 'carte'
                commande.paiement_confirme = True
                commande.date_paiement = datetime.now()
                commande.statut = 'payee'
                commande.validee = True
                commande.numero_suivi = _gen_suivi()
                commande.save()
                return redirect('confirmation_commande', commande_id=commande.id)

        elif mode == 'especes':
            commande.mode_paiement = 'especes'
            commande.paiement_confirme = False
            commande.statut = 'en_attente'
            commande.validee = True
            commande.numero_suivi = _gen_suivi()
            commande.save()
            return redirect('confirmation_commande', commande_id=commande.id)

        elif mode == 'virement':
            commande.mode_paiement = 'virement'
            commande.paiement_confirme = False
            commande.statut = 'en_attente'
            commande.validee = True
            commande.numero_suivi = _gen_suivi()
            commande.save()
            return redirect('confirmation_commande', commande_id=commande.id)

        else:
            error = "Veuillez choisir un mode de paiement."

    return render(request, 'magasin/checkout_paiement.html', {
        'commande': commande,
        'error': error,
        'nb_panier': _nb_panier(request.user),
    })


# Order confirmation page
@login_required(login_url='/magasin/login/')
def confirmation_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, utilisateur=request.user)
    return render(request, 'magasin/confirmation.html', {
        'commande': commande,
        'nb_panier': 0,
    })


# Manage user addresses
@login_required(login_url='/magasin/login/')
def mes_adresses(request):
    adresses = Adresse.objects.filter(utilisateur=request.user)
    return render(request, 'magasin/mes_adresses.html', {
        'adresses': adresses,
        'nb_panier': _nb_panier(request.user),
    })


@login_required(login_url='/magasin/login/')
def supprimer_adresse(request, adresse_id):
    adresse = get_object_or_404(Adresse, id=adresse_id, utilisateur=request.user)
    adresse.delete()
    messages.info(request, "Adresse supprimée.")
    return redirect('mes_adresses')


@login_required(login_url='/magasin/login/')
def definir_adresse_defaut(request, adresse_id):
    Adresse.objects.filter(utilisateur=request.user).update(par_defaut=False)
    adresse = get_object_or_404(Adresse, id=adresse_id, utilisateur=request.user)
    adresse.par_defaut = True
    adresse.save()
    messages.success(request, "Adresse par défaut mise à jour.")
    return redirect('mes_adresses')


# Validate order and redirect to checkout
@login_required(login_url='/magasin/login/')
def valider_commande(request):
    return redirect('checkout_livraison')


# Admin product management
def index(request):
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin/')
    else:
        form = ProduitForm()
    return render(request, 'magasin/majProduits.html', {'form': form})
