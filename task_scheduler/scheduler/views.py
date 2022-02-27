import csv
from rest_framework import viewsets
from scheduler.models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from django.db.models import Sum, Count



class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):        
        if self.action == 'shopping_cart':
            return PurchaseSerializer        
        return ProductSerializer

    @action(detail=True,
            methods=['POST', 'DELETE'],
            url_path='shopping_cart',
            url_name='shopping_cart')
            
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            product = Product.objects.get(id=pk)            
            data = {'user': request.user.id,
                    'product': product.id, 
                    'amount' : request.data['amount']}            
            serializer = PurchaseSerializer(
                data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        shopping_item = get_object_or_404(
            Purchase, user=request.user, product__id=pk)
        shopping_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(['get'], detail=False)                         
    def download_shopping_cart(self, request):
        products = (
            Purchase.objects
            .filter(user=request.user)
            .values_list('product__name', 'product__measurement_unit')
            .annotate(amount=Sum('amount')))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="Shopping_list.csv"')
        writer = csv.writer(response)
        writer.writerow(['Ингредиент', 'Единица измерения', 'Количество'])
        for product in products:
            writer.writerow(product)
        return response

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()    

    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PUT":
            return RecipeSerializer
        return RecipeSerializer

    @action(detail=True,
            methods=['GET', 'DELETE'],
            url_path='favorite',
            url_name='favorite')
            
    def favorite(self, request, pk):
        if request.method == 'GET':
            recipe = Recipe.objects.get(id=pk)
            data = {'user': request.user.id,
                    'recipe': recipe.id, }
            serializer = FavoriteSerializer(
                data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            favorite = get_object_or_404(
            Favorite, user=request.user, recipe__id=pk)
            print(favorite)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
