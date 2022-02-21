from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class Carte(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero = models.IntegerField()
    libelle = models.CharField(max_length=255)
    cin = models.CharField(max_length=22)
    code = models.IntegerField()
    solde = models.FloatField(default=0)
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.libelle

    def get_transactions_count(self):
        return Transaction.objects.filter(Q(from_carte=self) | Q(to_carte=self)).count()

    def get_valid_until(self):
        return self.valid_until.strftime("%d/%m/%Y %H:%M:%S")


class Transaction(models.Model):

    RETRAIT = 'retrait'
    VERSEMENT = 'versement'
    TRANSFER = 'transfer'

    TYPE_CHOICES = (
        (RETRAIT, 'Retrait'),
        (VERSEMENT, 'Versement'),
        (TRANSFER, 'Transfer'),
    )

    from_carte = models.ForeignKey(Carte, related_name='transfers', on_delete=models.CASCADE)
    to_carte = models.ForeignKey(Carte, related_name='receivers', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=22, choices=TYPE_CHOICES)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.type == self.RETRAIT:
            return f"{self.amount} {self.type} from {self.from_carte.libelle}"
        return f"{self.amount} {self.type} {self.from_carte.libelle} to {self.to_carte.libelle}"

    def get_date(self):
        return self.date.strftime("%d/%m/%Y %H:%M:%S")


class Demand(models.Model):

    ACTIVE = 'active'
    ACCEPTED = 'accepted'
    REFUSED = 'refused'

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (ACCEPTED, 'Accepted'),
        (REFUSED, 'Refused'),
    )

    demand_sender = models.ForeignKey(Carte, related_name='demands_sender', on_delete=models.CASCADE)
    demand_receiver = models.ForeignKey(Carte, related_name='demands_receiver', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=ACTIVE)
    comments = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.demand_sender} send demand for {self.amount} to {self.demand_receiver}"

    def get_date(self):
        return self.date.strftime("%d/%m/%Y %H:%M:%S")


class Favorite(models.Model):
    carte = models.ForeignKey(Carte, related_name='favorites', on_delete=models.CASCADE)
    favorite_carte = models.ForeignKey(Carte, related_name='favorite_carts', on_delete=models.CASCADE)
    comments = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.favorite_carte.libelle} is in favorite list of {self.carte.libelle}"

    def get_created_at(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")