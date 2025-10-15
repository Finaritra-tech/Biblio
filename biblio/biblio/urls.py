"""
URL configuration for biblio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from monApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('livre/liste/', liste_livres, name='liste_livres'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('ajouter_panier/<int:livre_id>/', ajouter_panier, name='ajouter_panier'),
    path('panier/', voir_panier, name='voir_panier'),
    path('panier/modifier/<int:panierlivre_id>/', modifier_quantite_panier, name='modifier_quantite_panier'),
    path('panier/supprimer/<int:panierlivre_id>/', supprimer_article_panier, name='supprimer_article_panier'),
    path('profil/', voir_profil, name='voir_profil'),
     path('profil/modifier/', modifier_profil, name='modifier_profil'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)