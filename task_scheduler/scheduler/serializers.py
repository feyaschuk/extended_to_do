from itertools import product
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.db import transaction

from scheduler.models import *
from users.models import *
from rest_framework.validators import UniqueTogetherValidator

class UserSerializer(serializers.ModelSerializer):    

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name')

    
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
    author = UserSerializer(read_only=True)
    products = ProductRecipeSerializer(many=True,
                                                  read_only=True,
                                                  source='ingr_amount')
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'products',
                  'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')
    
    def get_is_in_shopping_cart(self, obj):
        return self.bool_response(obj, Purchase)

    def bool_response(self, request_obj, main_obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return main_obj.objects.filter(user=request.user,
                                       recipe=request_obj.id).exists()
    
    def validate(self, data):
        method = self.context.get('request').method
        author = self.context.get('request').user
        recipe_name = data.get('name')
        products = self.initial_data.get('products')        

        if method in ('POST', 'PUT'):
            if (method == 'POST'
                and Recipe.objects.filter(author=author,
                                          name=recipe_name).exists()):
                raise serializers.ValidationError(
                    'Такой рецепт у вас уже есть!'
                )
            self.ingr_validate(products)
            

            if method == 'POST':
                data['author'] = author
            data['products'] = products
            
        if method == 'PATCH':
            if products:
                self.ingr_validate(products)
                data['products'] = products               
        return data

    def ingr_validate(self, products):
        ingrs_set = set()
        if not products:
            raise serializers.ValidationError(
                'Необходимо добавить хотя бы один ингредиент'
            )         
        for product in products:
            amount = product.get('amount')
            ingr_id = product.get('id')            
            if not Product.objects.filter(id=ingr_id).exists():
                raise serializers.ValidationError(
                    'Такого ингредиента еще нет, '
                    'обратитесь к администратору.'
                )
            if ingr_id in ingrs_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.'
                )
            try:
                int(amount)
            except ValueError:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть числом'
                )
            if int(amount) < 1:
                raise serializers.ValidationError(
                    'Убедитесь, что значение количества '
                    'ингредиента больше единицы'
                )
            ingrs_set.add(ingr_id)
            print(ingrs_set)

    def create(self, validated_data):
        image = validated_data.pop('image')
        products = validated_data.pop('products')           
          
        with transaction.atomic():
            recipe = Recipe.objects.create(image=image,
                                           **validated_data) 
        self.ingrs_only_create(products, recipe)       
        return recipe

    def ingrs_only_create(self, products, recipe):
        self.ingrs_create(products, recipe)


    def ingrs_create(self, products, recipe):         
        with transaction.atomic():
            for product in products:
                amount = product.get('amount')
                if not amount:
                    amount = 0
                ingr_amount = ProductRecipe.objects.create(
                    recipe=recipe,
                    product_id=product.get('id'),
                    amount=amount
                )
                ingr_amount.save()
    
    def update(self, instance, validated_data):
        attrs = {
            'image': None,
            'products': None
            
        }
        for attr in attrs:
            if attr in validated_data:
                attrs[attr] = validated_data.pop(attr)

        if attrs['image']:
            instance.image = attrs['image']
        instance = super().update(instance, validated_data)
        return instance


class PurchaseSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Purchase
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id        
        if self.Meta.model is Purchase:          
            answer = 'списке покупок'
        if (
            self.Meta.model.objects
            .select_related('recipe')
            .filter(user=request.user, recipe__id=recipe_id)
            .exists()
        ):
            raise serializers.ValidationError(f'Рецепт уже есть в {answer}')        
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortSerializer(instance.recipe, context=context).data


class ProductPurchaseSerializer(serializers.ModelSerializer):    
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ProductPurchase
        fields = ('user', 'product')

    def validate(self, data):
        request = self.context.get('request')              
        product_id = data['product'].id
        print(product_id)
        if self.Meta.model is ProductPurchase:          
            answer = 'списке покупок'
        if (
            self.Meta.model.objects
            .select_related('product')
            .filter(user=request.user, product__id=product_id)
            .exists()
        ):
            raise serializers.ValidationError(f'Продукт уже есть в {answer}')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortSerializer(instance.product, context=context).data









