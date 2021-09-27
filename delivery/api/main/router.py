from rest_framework import routers

from .views import RestaurantViewSet, MealViewSet, OrderViewSet, ComplaintViewSet
from ..cart.views import CartViewSet

router = routers.SimpleRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('restaurant', RestaurantViewSet, basename='restaurant')
router.register('meal', MealViewSet, basename='meal')
router.register('order', OrderViewSet, basename='order')
router.register('complaint', ComplaintViewSet, basename='complaint')

urlpatterns = []
urlpatterns += router.urls
