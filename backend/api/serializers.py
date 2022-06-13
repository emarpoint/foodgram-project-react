"""
Создание необходимых сериализаторов.
Creating the necessary sterilizers.
"""
from django.core.validators import RegexValidator
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Subscribe, Tag, TagRecipe)
from users.models import CustomUser


class CommonSubscribed(metaclass=serializers.SerializerMetaclass):
    """
    Класс для опредения подписки пользователя на автора.
    A class for determining the user's subscription to the author.
    """
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """
        Метод обработки параметра is_subscribed подписок.
        Method for processing the is_subscribed parameter of subscriptions.
        """
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if Subscribe.objects.filter(
                user=request.user, following__id=obj.id).exists():
            return True
        else:
            return False


class CommonRecipe(metaclass=serializers.SerializerMetaclass):
    """
    Класс для определения избранных рецептов и продуктов в корзине.
    A class for determining favorite recipes and products in the basket.
    """
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        """
        Метод обработки параметра is_favorited избранного.
        The method of processing the is_favorite parameter of the favorites.
        """
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if Favorite.objects.filter(user=request.user,
                                   recipe__id=obj.id).exists():
            return True
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        """
        Метод обработки параметра is_in_shopping_cart в списке покупок.
        The method of processing the is_in_shopping_cart parameter
        in the shopping list.
        """
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if ShoppingCart.objects.filter(user=request.user,
                                       recipe__id=obj.id).exists():
            return True
        else:
            return False


class CommonCount(metaclass=serializers.SerializerMetaclass):
    """
    Класс для опредения количества рецептов автора.
    A class for determining the number of author's recipes.
    """
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        """
        Метод подсчета количества рецептов автора.
        The method of counting the number of recipes of the author.
        """
        return Recipe.objects.filter(author__id=obj.id).count()


class RegistrationSerializer(UserCreateSerializer, CommonSubscribed):
    """
    Создание сериализатора модели пользователя.
    Creating a user model serializer.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\z',
                message="Недопустимый символ в slug.",
                ),
            ],


        )

    class Meta:
        """
        Мета параметры сериализатора модели пользователя.
        Meta parameters of the user model serializer.
        """
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {'is_subscribed': {'required': False}}

    def to_representation(self, obj):
        """
        Метод представления результатов сериализатора.
        The method of presenting the results of the sterilizer.
        """
        result = super(RegistrationSerializer, self).to_representation(obj)
        result.pop('password', None)
        return result


class IngredientSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора модели продуктов.
    Creating a product model serializer.
    """
    class Meta:
        """
        Мета параметры сериализатора модели продуктов.
        Meta parameters of the product model serializer.
        """
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        extra_kwargs = {'name': {'required': False},
                        'measurement_unit': {'required': False}}


class IngredientAmountSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора модели продуктов в рецепте для чтения.
    Creating a product model serializer in a recipe for reading.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        """
        Мета параметры сериализатора модели продуктов в рецепте.
        Meta parameters of the product model serializer in the recipe.
        """
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора продуктов с количеством для записи.
    Creating a serializer of products with a quantity to record.
    """
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        """
        Мета параметры сериализатора продуктов с количеством.
        Meta parameters of the serializer of products with quantity.
        """
        model = IngredientRecipe
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора модели тегов.
    Creating a tag model serializer.
    """
    slug = serializers.SlugField(
        max_length=50,
        # unique=True,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message="Недопустимый символ в slug.",

                ),
            ]
    )

    class Meta:
        """
        Мета параметры сериализатора модели тегов.
        Meta parameters of the tag model serializer.
        """
        model = Tag
        fields = ("id", "name", "color", "slug")
        extra_kwargs = {'name': {'required': False},
                        'slug': {'required': False},
                        'color': {'required': False}}


class FavoriteSerializer(serializers.Serializer):
    """
    Создание сериализатора избранных рецептов.
    Creating a serializer of selected recipes.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()
    image = Base64ImageField(max_length=None, use_url=False,)


class ShoppingCartSerializer(serializers.Serializer):
    """
    Создание сериализатора корзины.
    Creating a bucket serializer.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()
    image = Base64ImageField(max_length=None, use_url=False,)


class RecipeSerializer(serializers.ModelSerializer,
                       CommonRecipe):
    """
    Сериализатор модели рецептов.
    Recipe model sterilizer.
    """
    author = RegistrationSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientrecipes',
        many=True)
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        """
        Мета параметры сериализатора модели рецептов.
        Meta parameters of the recipe model serializer.
        """
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text',
                  'ingredients', 'tags', 'cooking_time',
                  'is_in_shopping_cart', 'is_favorited')


class RecipeSerializerPost(serializers.ModelSerializer,
                           CommonRecipe):
    """
    Сериализатор модели рецептов.
    Recipe model sterilizer.
    """
    author = RegistrationSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = IngredientAmountRecipeSerializer(
        source='ingredientrecipes', many=True)
    image = Base64ImageField(max_length=None, use_url=False,)

    class Meta:
        """
        Мета параметры сериализатора модели рецептов.
        Meta parameters of the recipe model serializer.
        """
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text',
                  'ingredients', 'tags', 'cooking_time',
                  'is_in_shopping_cart', 'is_favorited')

    def validate_ingredients(self, value):
        """
        Метод валидации продуктов в рецепте.
        A method for validating products in a recipe.
        """
        ingredients_list = []
        ingredients = value
        for ingredient in ingredients:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Количество должно быть равным или больше 1!')
            id_to_check = ingredient['ingredient']['id']
            ingredient_to_check = Ingredient.objects.filter(id=id_to_check)
            if not ingredient_to_check.exists():
                raise serializers.ValidationError(
                    'Данного продукта нет в базе!')
            if ingredient_to_check in ingredients_list:
                raise serializers.ValidationError(
                    'Данные продукты повторяются в рецепте!')
            ingredients_list.append(ingredient_to_check)
        return value

    def add_tags_and_ingredients(self, tags_data, ingredients, recipe):
        """
        Метод выполнения общих функции для создания и изменения рецептов.
        Method of performing common functions to create and modify recipes.
        """
        for tag_data in tags_data:
            recipe.tags.add(tag_data)
            recipe.save()
        for ingredient in ingredients:
            if not IngredientRecipe.objects.filter(
                    ingredient_id=ingredient['ingredient']['id'],
                    recipe=recipe).exists():
                ingredientrecipe = IngredientRecipe.objects.create(
                    ingredient_id=ingredient['ingredient']['id'],
                    recipe=recipe)
                ingredientrecipe.amount = ingredient['amount']
                ingredientrecipe.save()
            else:
                IngredientRecipe.objects.filter(
                    recipe=recipe).delete()
                recipe.delete()
                raise serializers.ValidationError(
                    'Данные продукты повторяются в рецепте!')
        return recipe

    def create(self, validated_data):
        """
        Метод создания рецептов.
        The method of creating recipes.
        """
        author = validated_data.get('author')
        tags_data = validated_data.pop('tags')
        name = validated_data.get('name')
        image = validated_data.get('image')
        text = validated_data.get('text')
        cooking_time = validated_data.get('cooking_time')
        ingredients = validated_data.pop('ingredientrecipes')
        recipe = Recipe.objects.create(
            author=author,
            name=name,
            image=image,
            text=text,
            cooking_time=cooking_time,
        )
        return self.add_tags_and_ingredients(tags_data, ingredients, recipe)

    def update(self, instance, validated_data):
        """
        Метод редактирования рецептов.
        Recipe editing method.
        """
        tags_data = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientrecipes')
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        instance = self.add_tags_and_ingredients(
            tags_data, ingredients, instance)
        super().update(instance, validated_data)
        instance.save()
        return instance


class RecipeMinifieldSerializer(serializers.ModelSerializer):
    """
    Сериализатор для упрощенного отображения модели рецептов.
    Sterilizer for simplified display of the recipe model.
    """
    class Meta:
        """
        Мета параметры сериализатора упрощенного
        отображения модели рецептов.
        Metaparameters of the simplified serializer
        displaying the recipe model.
        """
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class SubscriptionSerializer(serializers.ModelSerializer,
                             CommonSubscribed, CommonCount):
    """
    Сериализатор для списка подписок.
    A sterilizer for the subscription list.
    """
    recipes = serializers.SerializerMethodField()

    class Meta:
        """
        Мета параметры сериализатора списка подписок.
        Meta parameters of the subscription list serializer.
        """
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        """
        Метод получения данных рецептов автора,
        в зависимости от параметра recipes_limit.
        Method of obtaining the author's recipe data,
        depending on the recipes_limit parameter.
        """
        request = self.context.get('request')
        if request.GET.get('recipes_limit'):
            recipes_limit = int(request.GET.get('recipes_limit'))
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')[
                :recipes_limit]
        else:
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        return RecipeMinifieldSerializer(queryset, many=True).data
