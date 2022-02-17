from django.shortcuts import render
from rest_framework import viewsets
from scheduler.models import *
from .serializers import *

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class ProductPurchaseViewSet(viewsets.ModelViewSet):
    queryset = ProductPurchase.objects.all()
    serializer_class = ProductPurchaseSerializer

class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

class ProductRecipeViewSet(viewsets.ModelViewSet):
    queryset = ProductRecipe.objects.all()
    serializer_class = ProductRecipeSerializer
    
