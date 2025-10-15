from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator

def register_page(request):
    if request.user.is_authenticated:
        return redirect('liste_livres')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Compte créé avec succès pour' + user)
                return redirect('login')
        
    context = {'form': form}           
    return render(request, 'user/register.html', context)


def liste_livres(request):
    livres_list = Livre.objects.all()
    paginator = Paginator(livres_list, 8)
    page_number = request.GET.get('page')
    livres = paginator.get_page(page_number)

    return render(request, 'livre/liste_livres.html', {'livres': livres})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('liste_livres')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('liste_livres')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'user/login.html')

@login_required(login_url= 'login')
def logoutUser(request):
    logout(request)
    return redirect ('login')

def ajouter_panier(request, livre_id):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    
        
    else:
        if request.method == 'POST':
            livre_id_post = request.POST.get('livre_id')
            if livre_id_post:
                livre_id = int(livre_id_post)

            livre = get_object_or_404(Livre, id=livre_id)
            try:
                quantite = int(request.POST.get('quantite', 1))
            except ValueError:
                messages.error(request, "Quantité invalide.")
                return redirect('liste_livres')

            if quantite <= 0:
                messages.error(request, "La quantité doit être supérieure à zéro.")
                return redirect('liste_livres')

            if livre.stock < quantite:
                messages.error(request, f"Stock insuffisant pour « {livre.titre} ». Disponible : {livre.stock}")
                return redirect('liste_livres')

    
            panier, _ = Panier.objects.get_or_create(utilisateur=request.user)
            panier_livre, created = PanierLivre.objects.get_or_create(panier=panier, livre=livre)

            if not created:
                panier_livre.quantite += quantite
            else:
                panier_livre.quantite = quantite
            panier_livre.save()

            livre.stock -= quantite
            livre.save()

            messages.success(request, f"{quantite} exemplaire(s) de « {livre.titre} » ajouté(s) dans le panier.")
            return redirect('liste_livres')

        return redirect('liste_livres')
        
    
def liste_livres(request):
    query = request.GET.get('q')
    if query:
        livres_list = Livre.objects.filter(
            Q(titre__icontains=query) |
            Q(auteur__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        livres_list = Livre.objects.all()
   
    paginator = Paginator(livres_list, 8)  
    page_number = request.GET.get('page')
    livres = paginator.get_page(page_number)

    return render(request, 'livre/liste_livres.html', {
        'livres': livres,
        'query': query
    })
def voir_panier(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    
    else:

        panier = Panier.objects.filter(utilisateur=request.user).first()

        if panier:
            articles = PanierLivre.objects.filter(panier=panier).select_related('livre')
            total = sum(article.total for article in articles)
        else:
            articles = []
            total = 0

    return render(request, 'panier/liste_panier.html', {'articles': articles, 'total': total})

def modifier_quantite_panier(request, panierlivre_id):
    if request.method == "POST" and request.user.is_authenticated and not request.user.is_staff:
        article = get_object_or_404(PanierLivre, id=panierlivre_id)
        nouvelle_quantite = int(request.POST.get('quantite', article.quantite))

        if nouvelle_quantite <= 0:
            messages.error(request, "La quantité doit être supérieure à zéro.")
            return redirect('voir_panier')

        difference = nouvelle_quantite - article.quantite
        if difference > 0 and article.livre.stock < difference:
            messages.error(request, f"Stock insuffisant pour « {article.livre.titre} ». Disponible : {article.livre.stock}")
            return redirect('voir_panier')

        article.livre.stock -= difference
        article.livre.save()

        article.quantite = nouvelle_quantite
        article.save()

        messages.success(request, f"La quantité de « {article.livre.titre} » a été mise à jour.")
    return redirect('voir_panier')

def supprimer_article_panier(request, panierlivre_id):
    if request.method == "POST" and request.user.is_authenticated and not request.user.is_staff:
        article = get_object_or_404(PanierLivre, id=panierlivre_id)
        article.livre.stock += article.quantite
        article.livre.save()
        article.delete()
        messages.success(request, f"« {article.livre.titre} » a été retiré du panier.")
    return redirect('voir_panier')

@login_required
def voir_profil(request):
    profil = get_object_or_404(Profil, user=request.user)
    print("DEBUG - profil trouvé :", profil)
    return render(request, 'user/profil.html', {'profil': profil})

@login_required
def modifier_profil(request):
    user = request.user
    profil = user.profil

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        photo = request.FILES.get("photo")

        if username:
            user.username = username
        if email:
            user.email = email
        user.save()

        if photo:
            profil.photo = photo
            profil.save()

        return redirect("voir_profil")

    return redirect("voir_profil")