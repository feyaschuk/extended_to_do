import csv
from django.shortcuts import render
from rest_framework import viewsets
from scheduler.models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from django.db.models import Sum

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer    

    def get_serializer_class(self):
        if self.action == 'shopping_cart':
            return PurchaseSerializer        
        return self.serializer_class
    
    @action(['get'], detail=True)    
    def shopping_cart(self, request, pk=None):
        return self.alt_endpoint_create(request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.alt_endpoint_delete(request, pk, cart=True)

    @action(['get'], detail=False)                         
    def download_shopping_cart(self, request):
        products = (
            ProductRecipe.objects
            .select_related('product', 'recipe')
            .prefetch_related('purchases')
            .filter(recipe__purchases__user=request.user)
            .values_list('product__name', 'product__measurement_unit')
            .annotate(amount=Sum('amount'))
        )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="Your_shopping_list.csv"')

        writer = csv.writer(response)
        writer.writerow(['Ингредиент', 'Единица измерения', 'Количество'])
        for product in products:
            writer.writerow(product)

        return response

    def alt_endpoint_create(self, request, pk):
        verdict, recipe, user = self.recipe_validate(request, pk)
        if not verdict:
            return recipe

        data = {
            'user': user.id,
            'recipe': recipe.id,
        }

        serializer = self.get_serializer(data=data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def alt_endpoint_delete(self, request, pk, favorite=False, cart=False):
        verdict, obj = self.recipe_validate(request, pk, delete=True,
                                            favorite=favorite, cart=cart)
        if not verdict:
            return obj
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def recipe_validate(self, request, pk, delete=False,
                        favorite=False, cart=False):
        user = request.user
        if not Recipe.objects.filter(id=pk).exists():
            return False, Response({'error': 'Такого рецепта еще нет'},
                                   status=status.HTTP_400_BAD_REQUEST), None
        recipe = get_object_or_404(Recipe, id=pk)

        if delete:
            model_answer = {                
                'cart': (Purchase, 'списке покупок')
            }
            if cart:
                model, answer = model_answer.get('cart')
            if not model.objects.filter(user=user, recipe=recipe).exists():
                return False, Response(
                    {'error': f'Такого рецепта еще нет в вашем {answer}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return True, get_object_or_404(model, user=user, recipe=recipe)

        return True, recipe, user


