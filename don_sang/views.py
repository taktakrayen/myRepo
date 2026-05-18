from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Don, Hospital
from .forms import DonForm, LoginDonForm, RegisterDonForm, RechercheForm, HospitalForm, DonHospitalForm


def accueil_don(request):
    dons = Don.objects.select_related('donneur').all()
    form = RechercheForm(request.GET)

    if form.is_valid():
        groupe = form.cleaned_data.get('groupe_sanguin')
        ville = form.cleaned_data.get('ville')
        dispo = form.cleaned_data.get('disponibilite')
        if groupe:
            dons = dons.filter(groupe_sanguin=groupe)
        if ville:
            dons = dons.filter(ville__icontains=ville)
        if dispo:
            dons = dons.filter(disponibilite=dispo)

    # Stats pour le tableau de bord
    stats = {
        'total': Don.objects.count(),
        'disponibles': Don.objects.filter(disponibilite='disponible').count(),
        'villes': Don.objects.values('ville').distinct().count(),
        'groupes': Don.objects.values('groupe_sanguin').annotate(n=Count('id')).order_by('-n'),
    }

    return render(request, 'don_sang/accueil.html', {
        'dons': dons,
        'form': form,
        'stats': stats,
    })


@login_required(login_url='/don_sang/login/')
def faire_don(request):
    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.donneur = request.user
            don.save()
            messages.success(request, '✅ Votre don a été enregistré. Merci !')
            return redirect('mes_dons')
    else:
        form = DonForm()
    return render(request, 'don_sang/faire_don.html', {'form': form})


@login_required(login_url='/don_sang/login/')
def mes_dons(request):
    dons = Don.objects.filter(donneur=request.user).order_by('-date_don')
    return render(request, 'don_sang/mes_dons.html', {'dons': dons})


@login_required(login_url='/don_sang/login/')
def modifier_don(request, don_id):
    don = get_object_or_404(Don, id=don_id, donneur=request.user)
    if request.method == 'POST':
        form = DonForm(request.POST, instance=don)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Don mis à jour.')
            return redirect('mes_dons')
    else:
        form = DonForm(instance=don)
    return render(request, 'don_sang/modifier_don.html', {'form': form, 'don': don})


@login_required(login_url='/don_sang/login/')
def supprimer_don(request, don_id):
    don = get_object_or_404(Don, id=don_id, donneur=request.user)
    if request.method == 'POST':
        don.delete()
        messages.info(request, '🗑️ Don supprimé.')
        return redirect('mes_dons')
    return render(request, 'don_sang/supprimer_don.html', {'don': don})


def login_don(request):
    if request.user.is_authenticated:
        return redirect('accueil_don')
    form = LoginDonForm()
    error = None
    if request.method == 'POST':
        form = LoginDonForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'accueil_don')
                return redirect(next_url)
            else:
                error = "Identifiants incorrects."
    return render(request, 'don_sang/login.html', {'form': form, 'error': error})


def logout_don(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('accueil_don')


def register_don(request):
    if request.user.is_authenticated:
        return redirect('accueil_don')
    form = RegisterDonForm()
    error = None
    if request.method == 'POST':
        form = RegisterDonForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p1 = form.cleaned_data['password1']
            p2 = form.cleaned_data['password2']
            email = form.cleaned_data.get('email', '')
            if p1 != p2:
                error = "Les mots de passe ne correspondent pas."
            elif len(p1) < 6:
                error = "Mot de passe trop court (6 caractères minimum)."
            elif User.objects.filter(username=u).exists():
                error = "Ce nom d'utilisateur est déjà pris."
            else:
                user = User.objects.create_user(username=u, email=email, password=p1)
                login(request, user)
                messages.success(request, f"Bienvenue {u} !")
                return redirect('accueil_don')
    return render(request, 'don_sang/register.html', {'form': form, 'error': error})


def liste_hopitaux(request):
    hopitaux = Hospital.objects.all()
    return render(request, 'don_sang/hopitaux.html', {'hopitaux': hopitaux})


@login_required(login_url='/don_sang/login/')
def ajouter_hopital(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '🏥 Hôpital ajouté avec succès !')
            return redirect('liste_hopitaux')
    else:
        form = HospitalForm()
    return render(request, 'don_sang/ajouter_hopital.html', {'form': form})


@login_required(login_url='/don_sang/login/')
def modifier_hopital(request, hopital_id):
    hopital = get_object_or_404(Hospital, id=hopital_id)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hopital)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Hôpital mis à jour.')
            return redirect('liste_hopitaux')
    else:
        form = HospitalForm(instance=hopital)
    return render(request, 'don_sang/modifier_hopital.html', {'form': form, 'hopital': hopital})


@login_required(login_url='/don_sang/login/')
def supprimer_hopital(request, hopital_id):
    hopital = get_object_or_404(Hospital, id=hopital_id)
    if request.method == 'POST':
        hopital.delete()
        messages.info(request, '🗑️ Hôpital supprimé.')
        return redirect('liste_hopitaux')
    return render(request, 'don_sang/supprimer_hopital.html', {'hopital': hopital})


@login_required(login_url='/don_sang/login/')
def ajouter_donneur_hopital(request, hopital_id):
    hopital = get_object_or_404(Hospital, id=hopital_id)
    if request.method == 'POST':
        form = DonHospitalForm(request.POST)
        if form.is_valid():
            import secrets
            import unicodedata
            nom = form.cleaned_data['nom_donneur']
            nom_normalise = unicodedata.normalize('NFD', nom)
            nom_ascii = nom_normalise.encode('ascii', 'ignore').decode('ascii')
            username_base = nom_ascii.lower().replace(' ', '_')[:30]
            if not username_base:
                username_base = 'donneur'
            existing = set(User.objects.filter(
                username__startswith=username_base
            ).values_list('username', flat=True))
            username = username_base
            counter = 1
            while username in existing:
                suffix = f'_{counter}'
                username = username_base[:30 - len(suffix)] + suffix
                counter += 1
            password = secrets.token_urlsafe(10)
            parts = nom.split()
            user = User.objects.create_user(
                username=username,
                first_name=parts[0][:150] if parts else nom[:150],
                last_name=' '.join(parts[1:])[:150] if len(parts) > 1 else '',
                password=password,
            )
            Don.objects.create(
                donneur=user,
                hopital=hopital,
                groupe_sanguin=form.cleaned_data['groupe_sanguin'],
                ville=form.cleaned_data['ville'],
                telephone=form.cleaned_data['telephone'],
                age=form.cleaned_data['age'],
                disponibilite=form.cleaned_data['disponibilite'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, f'✅ Donneur « {nom} » ajouté à {hopital.nom} avec succès !')
            return redirect('detail_hopital', hopital_id=hopital.id)
    else:
        form = DonHospitalForm()
    return render(request, 'don_sang/ajouter_donneur_hopital.html', {'form': form, 'hopital': hopital})


def detail_hopital(request, hopital_id):
    hopital = get_object_or_404(Hospital, id=hopital_id)
    dons = Don.objects.filter(hopital=hopital).select_related('donneur').order_by('-date_don')
    return render(request, 'don_sang/detail_hopital.html', {'hopital': hopital, 'dons': dons})
