from rest_framework import serializers

from .models import Carte, Transaction, Demand, Favorite


class CarteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carte
        fields = (
            'id',
            'numero',
            'libelle'
        )


class CarteDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carte
        fields = (
            'id',
            'numero',
            'libelle',
            'solde',
            'cin',
            'get_transactions_count',
            'get_valid_until'
        )


class TransactionSerializer(serializers.ModelSerializer):
    to_carte = CarteSerializer(many=False, read_only=True)
    from_carte = CarteSerializer(many=False, read_only=True)

    class Meta:
        model = Transaction
        fields = (
            'id',
            'from_carte',
            'to_carte',
            'amount',
            'type',
            'get_date',
        )


class DemandSerializer(serializers.ModelSerializer):
    demand_sender = CarteSerializer(many=False)
    demand_receiver = CarteSerializer(many=False)

    class Meta:
        model = Demand
        fields = (
            'id',
            'demand_sender',
            'demand_receiver',
            'status',
            'comments',
            'amount',
            'get_date'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    favorite_carte = CarteSerializer(many=False)

    class Meta:
        model = Favorite
        fields = (
            'id',
            'favorite_carte',
            'comments',
            'get_created_at'
        )