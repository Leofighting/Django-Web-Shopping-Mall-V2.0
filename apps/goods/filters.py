# -*- coding:utf-8 -*-
__author__ = "leo"

import django_filters
from django.db.models import Q

from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """自定义商品过滤器"""
    pricemin = django_filters.NumberFilter(name="shop_price", lookup_expr="gte")
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr="lte")
    top_category = django_filters.NumberFilter(method="top_category_filter")

    @staticmethod
    def top_category_filter(queryset, name, value):
        queryset = queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))
        return queryset

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', "is_hot", "is_new"]
