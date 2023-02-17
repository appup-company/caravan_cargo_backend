from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class PaginationPackages(PageNumberPagination):
    page_size = 10
    max_page_size = 2000
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class PaginationAll(PageNumberPagination):
    page_size = 800
    max_page_size = 2000
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


# class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
#     pass


# class TestFilter(filters.FilterSet):
#     genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
#     year = filters.RangeFilter()

#     class Meta:
#         model = Product
#         fields = ['genres', 'year']