from django.shortcuts import render
from django.contrib.auth.models import User

from django.db.models import Q

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Carte, Transaction, Demand, Favorite
from .serializers import CarteSerializer, TransactionSerializer, CarteDetailsSerializer, DemandSerializer, \
    FavoriteSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        return self.queryset.filter(Q(from_carte=self.request.user.carte) | Q(to_carte=self.request.user.carte))\
            .order_by('-date')


class DemandViewSet(viewsets.ModelViewSet):
    serializer_class = DemandSerializer
    queryset = Demand.objects.all()

    def get_queryset(self):
        return self.queryset.filter(Q(demand_sender=self.request.user.carte) | Q(demand_receiver=self.request.user.carte))\
            .order_by('-date')


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def get_queryset(self):
        return self.queryset.filter(carte=self.request.user.carte).order_by('-created_at')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_favorite(request):

    try:
        numero = request.data['numero']
        comments = request.data['comments']
        carte = Carte.objects.get(numero=numero)
        if request.user.carte.favorites.filter(favorite_carte__numero=numero).count():
            return Response(
                "already exists",
                status=status.HTTP_200_OK
            )

        Favorite.objects.create(carte=request.user.carte, favorite_carte=carte, comments=comments)

        return Response(
            "success",
            status=status.HTTP_201_CREATED
        )
    except:
        return Response(
            "error, invalid data",
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def accept_demand(request, pk):
    response = add_transfer_for_accepted_demand(request)

    demand = Demand.objects.get(pk=pk)
    demand.status = Demand.ACCEPTED
    demand.save()

    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def refuse_demand(request, pk):
    demand = Demand.objects.get(pk=pk)
    demand.status = Demand.REFUSED
    demand.save()

    return Response(
        "success",
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_profile(request):

    profile = Carte.objects.get(user=request.user)
    serializer = CarteDetailsSerializer(profile, many=False)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_demand(request):
    try:
        demand_sender = request.user.carte
        demand_receiver = Carte.objects.get(numero=request.data['numero'])
        amount = request.data["amount"]
        comments = request.data["comments"]

        demand = Demand.objects.create(demand_sender=demand_sender, demand_receiver=demand_receiver, amount=amount,
                                       comments=comments)

        serializer = DemandSerializer(demand, many=False)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    except:
        return Response(
            {
                "message": "Invalid data, please try again",
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_transfer(request):
    try:
        to_carte = Carte.objects.get(numero=request.data['numero'])
        amount = request.data['amount']
        from_carte = request.user.carte

        if from_carte.solde < amount:
            return Response(
                {
                    "message": "Votre solde est insuffisante",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:

            transfer = Transaction.objects.create(from_carte=from_carte, to_carte=to_carte, amount=amount,
                                                  type=Transaction.TRANSFER)

            from_carte.solde -= amount
            from_carte.save()

            to_carte.solde += amount
            to_carte.save()

            serializer = TransactionSerializer(transfer)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
    except:
        return Response(
            {
                "message": "Numero carte entrée est incorrect",
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def validate_demand_data(request):

    try:
        to_carte = Carte.objects.get(numero=int(request.data['numero']))

        serializer = CarteSerializer(to_carte)

        return Response(
            {
                "message": "success",
                "carte": serializer.data
            },
            status=status.HTTP_200_OK
        )
    except:
        serializer = CarteSerializer(request.user.carte)
        return Response(
            {
                "message": "Numero carte entrée est incorrect",
                "carte": serializer.data
            },
            status=status.HTTP_400_BAD_REQUEST
        )



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def validate_transfer_data(request):


    try:
        to_carte = Carte.objects.get(numero=int(request.data['numero']))
        from_carte = Carte.objects.get(user=request.user)

        amount = request.data['amount']

        if from_carte.solde < amount:
            serializer = CarteSerializer(request.user.carte)
            return Response(
                {
                    "message": "Votre solde est insuffisante",
                    "carte": serializer.data
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:

            serializer = CarteSerializer(to_carte)

            return Response(
                {
                    "message": "success",
                    "carte": serializer.data
                },
                status=status.HTTP_200_OK
            )
    except:
        serializer = CarteSerializer(request.user.carte)
        return Response(
            {
                "message": "Numero carte entrée est incorrect",
                "carte": serializer.data
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def login(request):

    code = request.data['code']
    numero = request.data['numero']
    
    try:
        carte = Carte.objects.get(code=code, numero=numero)
        try:
            token = Token.objects.get(user=carte.user)
        except:
            token = Token.objects.create(user=carte.user)

        return Response(
            {
                'status': 'success',
                'token': str(token)
            },
            status.HTTP_200_OK
        )
    except:
        return Response(
            {
                'status': 'error',
                'message': 'no carte for this information'
            },
            status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def test(request):
    serializer = CarteSerializer(request.user.carte)
    return Response(
        {
            'status': 'success',
            'data': serializer.data,
        },
        status.HTTP_200_OK
    )


def add_transfer_for_accepted_demand(request):
    try:
        to_carte = Carte.objects.get(numero=request.data['numero'])
        amount = request.data['amount']
        from_carte = request.user.carte

        if from_carte.solde < amount:
            return Response(
                {
                    "message": "Votre solde est insuffisante",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:

            transfer = Transaction.objects.create(from_carte=from_carte, to_carte=to_carte, amount=amount,
                                                  type=Transaction.TRANSFER)

            from_carte.solde -= amount
            from_carte.save()

            to_carte.solde += amount
            to_carte.save()

            serializer = TransactionSerializer(transfer)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
    except:
        return Response(
            {
                "message": "Numero carte entrée est incorrect",
            },
            status=status.HTTP_400_BAD_REQUEST
        )
