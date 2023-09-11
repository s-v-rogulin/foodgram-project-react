from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from recipes.models import RecipeIngredientAmount


class CustomBaseSerializer(ModelSerializer):
    """Custom Serializer для избежания повторений"""

    image = Base64ImageField()

    def get_user_or_none(self):
        user = self.context['request'].user
        return None if user.is_anonymous else user

    def related_manager(
            self, related_name: str, field: str, value
    ) -> bool:
        user = self.get_user_or_none()
        if self.get_user_or_none():
            related_manager = getattr(user, related_name)
            return related_manager.filter(**{field: value}).exists()
        return False

    def add_inredients_amount(self, recipe, ingredients):
        RecipeIngredientAmount.objects.bulk_create(
            [RecipeIngredientAmount(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount']
            )for ingredient in ingredients]
        )

    def not_empty_field(self, field, value):
        if field := value:
            return field
        else:
            raise ValidationError({
                "{field}": "Нельзя ничего не выбрать!"
            })

    def get_tag_and_ingredient(self, data):
        tags = data.pop('tags')
        ingredients = data.pop('ingredients')
        return tags, ingredients

    def add_tag_and_ingredient_to_recipe(self, recipe, tags, ingredients):
        recipe.tags.set(tags)
        self.add_inredients_amount(
            recipe=recipe,
            ingredients=ingredients
        )
