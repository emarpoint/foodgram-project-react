"""
Создание view классов обработки запросов.
Creating view classes for processing requests.
"""

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Subscribe, Tag)
from users.models import CustomUser

from .filters import IngredientSearchFilter, RecipeFilters
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeSerializerPost,
                          RegistrationSerializer, ShoppingCartSerializer,
                          SubscriptionSerializer, TagSerializer)


class CreateUserView(UserViewSet):
    """
    Вьюсет обработки моделей пользователя.
    User model processing viewset.
    """
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return CustomUser.objects.all()


class SubscribeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки моделей подписок.
    Viewset for processing subscription models.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_list_or_404(CustomUser, following__user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Метод создания подписки.
        The method of creating a subscription.
        """
        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(CustomUser, id=user_id)
        Subscribe.objects.create(
            user=request.user, following=user)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """
        Метод удаления подписок.
        Method of deleting subscriptions.
        """
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет обработки моделей тэгов.
    Tag model processing viewset.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки моделей рецептов.
    Viewset for processing recipe models.
    """
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_class = RecipeFilters
    filter_backends = [DjangoFilterBackend, ]

    def perform_create(self, serializer):
        """
        Метод подстановки параметров автора при создании рецепта.
        The method of substituting the author's parameters when
        creating a recipe.
        """
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """
        Метод выбора сериализатора в зависимости от запроса.
        The method of selecting the serializer depending on the request.
        """
        if self.request.method == 'GET':
            return RecipeSerializer
        else:
            return RecipeSerializerPost


class IngredientViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки модели продуктов.
    Product model processing viewset.
    """
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, IngredientSearchFilter)
    pagination_class = None
    search_fields = ['^name', ]


class BaseFavoriteCartViewSet(viewsets.ModelViewSet):
    """
    Базовый вьюсет обработки модели корзины и избранных рецептов.
    The basic viewset for processing the basket model and selected recipes.
    """
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Метод создания модели корзины или избранных рецептов.
        A method for creating a basket model or selected recipes.
        """
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """
        Метод удаления объектов модели корзины или избранных рецептов.
        Method for deleting objects of the basket model or favorite recipes.
        """
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(BaseFavoriteCartViewSet):
    """
    Вьюсет обработки модели корзины.
    Basket model processing viewset.
    """
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    model = ShoppingCart


class FavoriteViewSet(BaseFavoriteCartViewSet):
    """
    Вьюсет обработки модели избранных рецептов.
    The viewset for processing the model of selected recipes.
    """
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    model = Favorite


class DownloadShoppingCart(viewsets.ModelViewSet):
    """
    Сохранение файла списка покупок.
    Saving a shopping list file.
    """
    permission_classes = [permissions.IsAuthenticated]

    def download_pdf(self, result):
        """
        Метод сохранения списка покупок в формате PDF.
        A method for saving a shopping list in PDF format.
        """
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'
            ] = ('attachment; filename="somefilename.pdf"')
        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response, pagesize=A4)
        left_position = 50
        top_position = 700
        # Connecting fonts from the data folder
        pdfmetrics.registerFont(TTFont('FreeSans',
                                       'data/FreeSans.ttf'))
        p.setFont('FreeSans', 25)
        # Draw things on the PDF. Here's where the PDF generation happens.
        p.drawString(left_position, top_position + 40, "Список покупок:")

        # Adding a shopping list from the database
        for number, item in enumerate(result, start=1):
            pdfmetrics.registerFont(
                TTFont('Miama Nueva', 'data/Miama Nueva.ttf')
                )
            p.setFont('Miama Nueva', 14)
            p.drawString(
                left_position,
                top_position,
                f'{number}.  {item["ingredient__name"]} - '
                f'{item["ingredient_total"]}'
                f'{item["ingredient__measurement_unit"]}'
            )
            top_position = top_position - 40

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response

    def download(self, request):
        """
        Метод создания списка покупок.
        The method of creating a shopping list.

        """
        result = IngredientRecipe.objects.filter(
            recipe__carts__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
                'ingredient__name').annotate(ingredient_total=Sum('amount'))
        return self.download_pdf(result)
