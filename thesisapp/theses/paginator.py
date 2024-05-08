from rest_framework.pagination import PageNumberPagination


class PaginatorTheses(PageNumberPagination):
    page_size = 5