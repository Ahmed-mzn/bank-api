from django.contrib import admin

from .models import Carte, Transaction, Demand, Favorite

admin.site.register(Carte)
admin.site.register(Transaction)
admin.site.register(Demand)
admin.site.register(Favorite)
