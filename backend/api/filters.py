"""
Настройка пользовательских фильтров.
"""

# from django_filters import rest_framework as django_filter
from django_filters.rest_framework import filters
from rest_framework import filters

from users.models import CustomUser
from recipes.models import Recipe


class RecipeFilters(filters.FilterSet):
    """
    Настройка фильтров модели рецептов.
    """
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        """
        Мета параметры фильтров модели рецептов.
        """
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    # def get_is_favorited(self, queryset, name, value):
    #     """
    #     Метод обработки фильтров параметра is_favorited.
    #     """
    #     if self.request.user.is_authenticated and value:
    #         return queryset.filter(favorites__user=self.request.user)
    #     return queryset

    def get_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """
        Метод обработки фильтров параметра is_in_shopping_cart.
        """
        if self.request.user.is_authenticated and value:
            return queryset.filter(carts__user=self.request.user)
        return queryset.all()


class IngredientSearchFilter(filters.SearchFilter):
    """
    Настройка фильтра поиска модели продуктов.
    Configuring the product model search filter.
    """
    search_param = 'name'
