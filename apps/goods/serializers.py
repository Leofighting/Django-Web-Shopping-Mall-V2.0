# -*- coding:utf-8 -*-
__author__ = "leo"

from rest_framework import serializers

from goods.models import Goods, GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    """序列化：商品分类"""

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    """序列化：商品"""
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = "__all__"

