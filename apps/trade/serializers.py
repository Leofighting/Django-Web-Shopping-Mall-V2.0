# -*- coding:utf-8 -*-
__author__ = "leo"

import time
from random import Random

from rest_framework import serializers

from MxShopV2.settings import app_private_key_path, alipay_public_key_path
from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from utils.alipay import AliPay


class ShoppingCartDetailSerializer(serializers.Serializer):
    """序列化：购物车详情"""
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = ["goods", "nums"]


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


class OrderSerializer(serializers.ModelSerializer):
    """序列化：订单"""

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    def generate_order_sn(self):
        """生成订单号"""
        random_int = Random()
        order_sn = "{time_str}{user_id}{random_str}".format(
            time_str=time.strftime("%Y%m%d%H%M%S"),
            user_id=self.context["request"].user.id,
            random_str=random_int.randint(10, 100))

        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    """序列化：订单商品详情"""
    goods = GoodsSerializer(many=True)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    """序列化：订单详情"""
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"
