# Generated by Django 3.2 on 2023-09-04 22:16

import core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_to_shopping_cart_date', models.DateTimeField(auto_now=True, verbose_name='Дата добавления в корзину')),
            ],
            options={
                'verbose_name': 'Рецепт в корзине',
                'verbose_name_plural': 'Рецепты в корзине',
                'ordering': ('add_to_shopping_cart_date',),
            },
        ),
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_to_favorite_date', models.DateTimeField(auto_now=True, verbose_name='Дата добавления в избранное')),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
                'ordering': ('add_to_favorite_date',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Напишите название ингредиента', max_length=200, validators=[core.validators.TwoCharValidator(2), core.validators.CyrillicCharRegexValidator()], verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(help_text='Введите единицу измерения', max_length=200, validators=[core.validators.MinMeasurementUnitLenghtValidator(1), core.validators.CyrillicCharRegexValidator()], verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Придумайте название рецепта', max_length=200, validators=[core.validators.TwoCharValidator(2)], verbose_name='Название')),
                ('image', models.ImageField(upload_to='recipes/images/', verbose_name='Картинка')),
                ('text', models.TextField(help_text='Опишите рецепт', validators=[core.validators.TwoCharValidator(2)], verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Введите время приготовления рецепта', validators=[core.validators.MinCookingTimeValueValidator(1)], verbose_name='Время приготовления (в минутах)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('pub_date', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Придумай название для тега', max_length=200, unique=True, validators=[core.validators.TwoCharValidator(2), core.validators.CyrillicCharRegexValidator()], verbose_name='Название')),
                ('color', models.CharField(help_text='Пропишите цвет в HEX формате', max_length=7, validators=[core.validators.MinTagColorLenghtValidator(4), core.validators.TagColorRegexValidator()], verbose_name='Цвет в HEX')),
                ('slug', models.SlugField(help_text='Введите слаг тега', max_length=200, unique=True, validators=[core.validators.TwoCharValidator(2), core.validators.LatinCharRegexValidator()], verbose_name='Уникальный слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredientAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[core.validators.MinAmountValidator(1)], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Кол-во ингредиента в рецепте',
                'ordering': ('recipe', 'ingredient'),
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients_in_recipe', through='recipes.RecipeIngredientAmount', to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Выбирете теги для рецепта', related_name='recipe_tags', to='recipes.Tag', verbose_name='Тег'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_name_measurement_unit'),
        ),
        migrations.AddField(
            model_name='favoriterecipe',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт, который нужно добавить в избранное', on_delete=django.db.models.deletion.CASCADE, related_name='in_favorite', to='recipes.recipe', verbose_name='Избранный рецепт'),
        ),
        migrations.AddField(
            model_name='favoriterecipe',
            name='user',
            field=models.ForeignKey(help_text='Пользователь, в чье избранное добавляется рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipe_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='cart',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт, который нужно добавить в корзину', on_delete=django.db.models.deletion.CASCADE, related_name='in_shopping_cart', to='recipes.recipe', verbose_name='Рецепт в корзине'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(help_text='Пользователь, в чью корзину добавляется рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredientamount',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_fevorite_user_recipe'),
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_cart_user_recipe'),
        ),
    ]
