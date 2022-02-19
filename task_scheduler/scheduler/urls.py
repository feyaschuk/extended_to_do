from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import  *

router_v1 = DefaultRouter(trailing_slash='optional')
router_v1.register('shops/?', ShopViewSet, basename='shop')
router_v1.register('products/?', ProductViewSet, basename='product')
router_v1.register('recipes/?', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
    path('', include(router_v1.urls)),
]