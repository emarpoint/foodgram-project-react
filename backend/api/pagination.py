""""
Создание пагинатора.
Creating a paginator.
"""

from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Создание пагинатора, наследуемого от PageNumberPagination.
    Creating a paginator inherited from PageNumber Pagination.
    """
    page_size = 6
    page_size_query_param = 'limit'
