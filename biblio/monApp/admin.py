from django.contrib import admin
from .models import*
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Livre)
admin.site.register(Panier)
admin.site.register(PanierLivre)
admin.site.register(Profil)


