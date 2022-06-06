from users.models import CustomUser
from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator)
from colorfield.fields import ColorField


class Ingredient(models.Model):
    """
    Создание модели продуктов.
    Creating a product model.
    """
    name = models.CharField(
        max_length=256,
        verbose_name="Название ингридиента",
        help_text="Введите название ингридиента"
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
        help_text='Введите единицы измерения')

    class Meta:
        """
        Параметры модели.
        Model parameters.
        """
        verbose_name = 'Продукт',
        verbose_name_plural = 'Продукты'

    def __str__(self):
        """
        Метод строкового представления модели.
        Method of string representation of the model.
        """
        return self.name


class Tag(models.Model):
    """
    Создание модели тэгов.
    Creating a tag model.
    """
    name = models.CharField(
        max_length=256,
        verbose_name="Название тэга",
        help_text="Введите название тэга"
    )
    color = ColorField(
        default='#FF0000',
        format='hex',
        verbose_name='Цвет',
        help_text='Введите цвет тэга'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Текстовый идентификатор тега',
        help_text='Введите текстовый идентификатор тега'
    )

    class Meta:
        """
        Параметры модели.
        Model parameters.
        """
        verbose_name = "Тэг",
        verbose_name_plural = "Тэги"

    def __str__(self):
        """
        Метод строкового представления модели.
        Method of string representation of the model.
        """
        return self.slug


class Recipe(models.Model):
    """
    Создание модели рецептов.
    Creating a recipe model.
    """
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name="Автор",
        help_text="Введите имя автора"
    )
    name = models.CharField(
        max_length=256,
        verbose_name="Название рецепта",
        help_text="Введите название рецепта"
    )
    image = models.ImageField(
        verbose_name="Загрузить фото",
        upload_to='recipes/image/',
        help_text="Загрузите картинку блюда."
    )
    text = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание блюда.",
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Теги',
        help_text='Выберите тег рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Продукты в рецепте',
        help_text='Выберите продукты рецепта.'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(500)
        ],
        verbose_name="Время приготовления",
        help_text="Введите время приготовления в минутах."
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Добавить дату создания.')

    class Meta:
        """
        Параметры модели.
        Model parameters.
        """
        verbose_name = "Рецепт",
        verbose_name_plural = "Создание рецепта"
        ordering = ('-pub_date', )

    def __str__(self):
        """
        Метод строкового представления модели.
        Method of string representation of the model.
        """
        return self.name


class ShoppingCart(models.Model):
    """
    Создание модели списка покупок.
    Creating a shopping list model.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберете пользователя.'

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепты',
        help_text='Выберите рецепт для добавления в список покупок.'

    )

    class Meta:
        """
        Параметры модели.
        Model parameters.
        """
        verbose_name = "Список покупок",
        verbose_name_plural = "Создание списка покупок"

    def __str__(self):
        """
        Метод строкового представления модели.
        Method of string representation of the model.
        """
        return f'{self.user} {self.recipe}'


class IngredientRecipe(models.Model):
    """
    Создание модели продуктов в рецепте.
    Creating a product model in a recipe.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Продукты рецепта',
        help_text='Добавить продукты рецепта в список.')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Выберите рецепт',
        related_name='ingredientrecipes',

    )
    amount = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество продукта',
        help_text='Введите количество продукта'
    )

    class Meta:
        """
        Параметры модели.
        Model parameters.
        """
        verbose_name = 'Продукты в рецепте'
        verbose_name_plural = 'Продукты в рецепте'

    def __str__(self):
        """"
        Метод строкового представления модели.
        Method of string representation of the model.
        """
        return f'{self.ingredient} {self.recipe}'


class TagRecipe(models.Model):
    """
    Создание модели тегов рецепта.
    Creating a recipe tag model.
    """
    tags = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Теги',
        help_text='Выберите теги рецепта',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Выберите рецепт')

    class Meta:
        """
        Параметры модели.
        Model parameters.
        """
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = [
            models.UniqueConstraint(fields=['tags', 'recipe'],
                                    name='unique_tagrecipe')
        ]

    def __str__(self):
        """"
        Метод строкового представления модели.
        Method of string representation of the model.
        """
        return f'{self.tags} {self.recipe}'


class Favorite(models.Model):
    """
    Создание модели избранных рецептов.
    Creating a model of favorite recipes.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        """
        Параметры модели.
        Model parameters.
        """
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        """"
        Метод строкового представления модели.
        Method of string representation of the model.
        """
        return f'{self.recipe} {self.user}'


class Subscribe(models.Model):
    """
    Создание модели подписок.
    Creating a subscription model.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Выберите пользователя, который подписывается.'

    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Выберите автора, на которого подписываются.'

    )

    class Meta:
        """
        Параметры модели.
        Model parameters.
        """
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        """"
        Метод строкового представления модели.
        Method of string representation of the model.
        """
        return f'{self.user}'
