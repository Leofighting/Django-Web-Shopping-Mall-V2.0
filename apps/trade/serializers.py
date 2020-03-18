# -*- coding:utf-8 -*-
__author__ = "leo"

from rest_framework import serializers

from goods.models import Goods
from trade.models import ShoppingCart


class ShoppingCartSerializer(serializers.Serializer):
    """序列化：购物车"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1,
                                    label="购买数量",
                                    error_messages={
                                        "min_value": "至少要有 1 件商品~",
                                        "required": "请选择购买数量~"
                                    })

    goods = serializers.PrimaryKeyRelatedField(required=True,
                                               label="商品",
                                               queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        """修改商品数量"""
        instance.nums = validated_data["nums"]
        instance.save()
        return instance
