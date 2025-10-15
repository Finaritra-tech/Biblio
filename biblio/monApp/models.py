from django.db import models
from django.contrib.auth.models import User

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    couverture = models.ImageField(upload_to='couverture/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.titre

class Panier(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paniers')
    date_creation = models.DateTimeField(auto_now_add=True)
    livres = models.ManyToManyField('Livre', through='PanierLivre', related_name='paniers')

    def __str__(self):
        return f"Panier de {self.utilisateur.username}"


class PanierLivre(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.livre.titre} (Panier de {self.panier.utilisateur.username})"

    @property
    def total(self):
        return self.livre.prix * self.quantite
    
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    photo = models.ImageField(upload_to='profil/', default='profil/defaut.jpeg')

    def __str__(self):
        return f"Profil de {self.user.username}"