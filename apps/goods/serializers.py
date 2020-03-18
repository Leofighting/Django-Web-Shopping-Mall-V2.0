# -*- coding:utf-8 -*-
__author__ = "leo"

from rest_framework import serializers

from goods.models import Goods, GoodsCategory, HotSearchWords, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    """序列化：商品分类-二级"""

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """序列化：商品分类-二级"""
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """序列化：商品分类-一级"""
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    """序列化：商品图片"""
    class Meta:
        model = GoodsImage
        fields = ["image"]


class GoodsSerializer(serializers.ModelSerializer):
    """序列化：商品"""
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"
