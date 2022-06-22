from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Subscribe, Tag, TagRecipe)


class IngredientRecipeInline(admin.TabularInline):
    """
    Параметры настроек админ зоны
    модели ингредиентов в рецепте.
    """
    model = IngredientRecipe
    extra = 0


class TagRecipeInline(admin.TabularInline):
    """
    Параметры настроек админ зоны
    модели тэгов рецепта.
    """
    model = TagRecipe
    extra = 0


class IngredientAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны продуктов.
    """
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class TageAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны тэгов.
    """
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('name',)
    list_display = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'
    search_fields = ('name', )


class FavoriteAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны избранных рецептов.
    """
    list_display = ('user', 'recipe')
    search_fields = ('user', )
    empty_value_display = '-пусто-'
    list_filter = ('user',)


class RecipeAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны рецептов.
    """
    inlines = (IngredientRecipeInline, TagRecipeInline,)

    list_display = ('name', 'author', 'cooking_time',
                    'id', 'count_favorite', 'pub_date')
    search_fields = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'
    list_filter = ('name', 'author', 'tags')

    def count_favorite(self, obj):
        """
        Метод для подсчета общего числа
        добавлений этого рецепта в избранное.
        """
        return Favorite.objects.filter(recipe=obj).count()
    count_favorite.short_description = 'Число добавлении в избранное'


class ShoppingCartAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны списка покупок.
    """
    list_filter = ('recipe',)
    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'
    search_fields = ('recipe', )


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user', )
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TageAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
