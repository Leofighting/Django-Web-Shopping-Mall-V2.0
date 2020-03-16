from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from goods.filters import GoodsFilter
from goods.models import Goods
from goods.serializers import GoodsSerializer


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表
    """
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    queryset = Goods.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = GoodsFilter
    search_fields = ["name", "goods_brief", "goods_desc"]
    ordering_fields = ["sold_num", "add_time"]


