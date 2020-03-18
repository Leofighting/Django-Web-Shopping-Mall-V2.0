# -*- coding:utf-8 -*-
__author__ = "leo"

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from user_operation.models import UserFav, UserLeavingMessage, UserAddress


class UserFavSerializer(serializers.ModelSerializer):
    """序列化：添加用户收藏功能"""

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user", "goods"),
                message="该商品已经收藏~"
            )
        ]
        fields = ("user", "goods", "id")


class UserFavDetailSerializer(serializers.ModelSerializer):
    """序列化：用户收藏详情"""
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    """序列化：用户留言"""

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserLeavingMessage
        fields = ["id", "user", "message_type", "subject", "message", "file", "add_time"]


class AddressSerializer(serializers.ModelSerializer):
    """序列化：用户地址信息"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    signer_mobile = serializers.CharField(max_length=11, min_length=11)

    class Meta:
        model = UserAddress
        fields = ["id", "user", "province", "city", "district", "address", "signer_name", "signer_mobile"]
