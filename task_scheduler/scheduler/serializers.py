from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from scheduler.models import *
from users.models import *
from rest_framework.validators import UniqueTogetherValidator

class ShopSerializer(serializers.ModelSerializer):    
    class Meta:
        fields = ('id', 'name', 'adress')
        model = Shop

class ProductSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    class Meta:
        fields = '__all__'
        model = Product
        validators = [
            UniqueTogetherValidator(
                queryset=Product.objects.all(),
                fields=('name', 'measurement_unit')
            )]

class ProductRecipeSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True, source='product')    
    
    def get_product(self, obj):
        return obj.product.name

    class Meta:
        fields = ('id', 'product', 'amount')
        model = ProductRecipe


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    products = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_products(self, obj):
        return ProductRecipeSerializer(
            ProductRecipe.objects.filter(recipe=obj).all(), many=True
        ).data

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(recipe_id=obj.id).exists()

    class Meta:
        fields = '__all__'
        model = Recipe


class ProductPurchaseSerializer(serializers.ModelSerializer):    
    product = serializers.SerializerMethodField()
    
    def get_product(self, obj):
        return ProductSerializer(
            Product.objects.filter(name=obj).all(), many=True
        ).data

    class Meta:
        fields = '__all__'
        model = ProductPurchase

class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    products = serializers.PrimaryKeyRelatedField(queryset=ProductPurchase.objects.all())
    
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe', 'products')

    def to_representation(self, instance):
        a=RecipeShortSerializer(instance.recipe).data
        b =ProductPurchaseSerializer(instance.products).data
        return a,b




