# -*- coding:utf-8 -*-
__author__ = "leo"

import django_filters

from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """自定义商品过滤器"""
    price_min = django_filters.NumberFilter(name="shop_price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(name="shop_price", lookup_expr="lte")

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max']
