from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import login, test, TransactionViewSet, add_transfer, get_profile, validate_transfer_data, \
    DemandViewSet, FavoriteViewSet, add_demand, validate_demand_data, refuse_demand, accept_demand, add_favorite

router = DefaultRouter()
router.register('transactions', TransactionViewSet, basename='TransactionViewSet')
router.register('demands', DemandViewSet, basename='DemandViewSet')
router.register('favorites', FavoriteViewSet, basename='FavoriteViewSet')


urlpatterns = [
    path('login', login, name='login'),
    path('add_transfer', add_transfer, name='add_transfer'),
    path('add_demand', add_demand, name='add_demand'),
    path('add_favorite', add_favorite, name='add_favorite'),
    path('refuse_demand/<int:pk>', refuse_demand, name='refuse_demand'),
    path('accept_demand/<int:pk>', accept_demand, name='accept_demand'),
    path('get_profile', get_profile, name='get_profile'),
    path('validate_transfer_data', validate_transfer_data, name='validate_transfer_data'),
    path('validate_demand_data', validate_demand_data, name='validate_demand_data'),
    path('test', test, name='test'),
    path('', include(router.urls)),
]