from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer, ReadRecipeSerializer,
                             TagSerializer, WriteRecipeSerializer)
from core.constants import ARGUMENTS_TO_ACTION_DECORATORS
from core.servises import (create_and_download_shopping_cart,
                           creation_favorite_or_shopping_cart_recipe,
                           delete_recipe_from_favorite_or_shopping_cart)
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Cart, FavoriteRecipe, Ingredient, Recipe, Tag
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class IngredientViewSet(ReadOnlyModelViewSet):
    """ViewSet модели ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    """ViewSet модели тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    """ViewSet модели рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReadRecipeSerializer
        return WriteRecipeSerializer

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('post_del'))
    def favorite(self, request, pk):
        if request.method == 'POST':
            return creation_favorite_or_shopping_cart_recipe(
                model=FavoriteRecipe, user=request.user, id=pk
            )
        return delete_recipe_from_favorite_or_shopping_cart(
            model=FavoriteRecipe, user=request.user, id=pk
        )

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('post_del'))
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return creation_favorite_or_shopping_cart_recipe(
                model=Cart, user=request.user, id=pk
            )
        return delete_recipe_from_favorite_or_shopping_cart(
            model=Cart, user=request.user, id=pk
        )

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('get'))
    def download_shopping_cart(self, request):
        return create_and_download_shopping_cart(request.user)
