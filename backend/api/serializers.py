import re

from django.db.models import F
from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField)
from rest_framework.status import HTTP_400_BAD_REQUEST

from core.constants import (MIN_AMOUNT,
                            MIN_COOKING_TIME,
                            MAX_COOKING_TIME)
from core.serializers import CustomBaseSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredientAmount, Tag
from users.models import User


class RecipeShortSerializer(CustomBaseSerializer):
    """Сокращенная модель Рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Custom Djoser Serializer для создания пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    """Custom Djoser Serializer для пользователя."""

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return (
            user.subscriber_user.filter(author=obj).exists()
        )


class SubscriptionSerializer(CustomUserSerializer):
    """Serializer подписки на автора."""

    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'recipes',
        )

    def get_recipes_count(self, obj):
        return obj.recipe_author.count()

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_limit = request.GET.get('recipes_limit')
        recipes = obj.recipe_author.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeShortSerializer(
            recipes, many=True, read_only=True
        ).data

    def validate(self, data):
        author = self.instance
        user = self.context['request'].user
        if user.subscriber_user.filter(author=author).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого автора!',
                code=HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='К сожалению, вы не можете подписаться на себя!',
                code=HTTP_400_BAD_REQUEST
            )
        return data


class TagSerializer(ModelSerializer):
    """Serializer модели тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('__all__',)


class IngredientSerializer(ModelSerializer):
    """Serializer модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('__all__',)


class RecipeIngredientAmountSerializer(ModelSerializer):
    """Serializer количества игредиента в рецепте."""

    id = IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredientAmount
        fields = (
            'id',
            'amount',
        )


class ReadRecipeSerializer(CustomBaseSerializer):
    """Serializer для просмотра рецепта."""

    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    ingredients = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        return (
            self.related_manager(
                'favorites', 'recipe', obj
            )
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.related_manager(
                'shopping_cart', 'recipe', obj
            )
        )

    def get_ingredients(self, obj):
        return (
            obj.ingredients.values(
                'id',
                'name',
                'measurement_unit',
                amount=F('recipeingredientamount__amount')
            )
        )


class WriteRecipeSerializer(CustomBaseSerializer):
    """Serializer для создания рецепта."""

    ingredients = RecipeIngredientAmountSerializer(many=True)
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    cooking_time = IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'author',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, value):
        ingredients = self.Not_empty_field(
            field='ingredients', value=value
        )
        if not ingredients:
            raise ValidationError({
                "ingredients": "Нельзя добавлять без ингредиентов!"
            })
        ingredients_in_recipe = []
        for ingredient in ingredients:
            if ingredient in ingredients_in_recipe:
                raise ValidationError({
                    "ingredients": "Вы уже добавили этот ингредиент!"
                })
            if int(ingredient['amount']) < MIN_AMOUNT:
                raise ValidationError({
                    "amount": "Количесво ингредиента не может быть меньше 1!"
                })
            ingredients_in_recipe.append(ingredient)
        return value

    def validate_name(self, value):
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s]+$', value):
            raise ValidationError({
                "name": "Название рецепта должно состоять только из букв!"
            })
        return value

    def validate_cooking_time(self, value):
        if value < MIN_COOKING_TIME:
            raise ValidationError({
                "cooking_time": "Время приготовления не может быть меньше 1!"
            })
        if value > MAX_COOKING_TIME:
            raise ValidationError({
                "cooking_time":
                    "Время приготовления не может быть больше 1000!"
            })
        return value

    def validate_tags(self, value):
        tags = self.Not_empty_field(
            field='tags', value=value
        )
        if not tags:
            raise ValidationError({
                "tags": "Добавьте хотя бы один тег!"
            })
        tags_in_recipe = []
        for tag in tags:
            if tag in tags_in_recipe:
                raise ValidationError({
                    "tags": "Этот тег уже выбран!"
                })
            tags_in_recipe.append(tag)
        return value

    @transaction.atomic
    def create(self, validated_data):
        tags, ingredients = self.get_tag_and_ingredient(
            data=validated_data
        )
        recipe = Recipe.objects.create(**validated_data)
        self.add_tag_and_ingredient_to_recipe(
            recipe=recipe, tags=tags, ingredients=ingredients
        )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            instance.tags.clear()
            instance.tags.set(validated_data.pop('tags'))
        if 'ingredients' in validated_data:
            instance.recipeingredientamount_set.all().delete()
            self.add_inredients_amount(
                recipe=instance,
                ingredients=validated_data.pop('ingredients')
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context['request']
        context = {'request': request}
        return ReadRecipeSerializer(
            instance=instance,
            context=context,
        ).data
