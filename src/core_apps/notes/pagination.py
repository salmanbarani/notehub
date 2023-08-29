from rest_framework.pagination import PageNumberPagination


class NotePagination(PageNumberPagination):
    page_size = 5
