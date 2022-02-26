from asyncore import read
from itertools import product
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from scheduler.models import *
from users.serializers import CustomUserSerializer
from rest_framework.validators import UniqueTogetherValidator

   
class ShopSerializer(serializers.ModelSerializer):    
    class Meta:
        fields = ('id', 'name', 'adress')
        model = Shop


class ProductSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField() 
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_in_shopping_cart(self, obj):
        return ProductPurchase.objects.filter(product_id=obj.id).exists()

    class Meta:
        fields = '__all__'
        model = Product
        validators = [
            UniqueTogetherValidator(
                queryset=Product.objects.all(),
                fields=('name', 'measurement_unit')
            )]

class ProductRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')
    measurement_unit = serializers.ReadOnlyField(source='product'
                                                 '.measurement_unit')
    category = serializers.ReadOnlyField(source='product.category')                                           
    class Meta:
        model = ProductRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount', 'category')


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    products = ProductRecipeSerializer(many=True,
                                                  read_only=True,
                                                  source='amount')
    is_favorited = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'products',
                  'is_favorited',
                  'name', 'image', 'text', 'cooking_time')
    
    def get_is_favorited(self, obj):
        return Favorite.objects.filter(recipe_id=obj.id).exists()
 

class ProductPurchaseSerializer(serializers.ModelSerializer):    
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = ProductPurchase
        fields = ('user', 'product', 'amount')


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return RecipeShortSerializer(instance.recipe).data  

    








