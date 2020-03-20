from datetime import datetime

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
from rest_framework.views import APIView
from django.shortcuts import redirect

from MxShopV2.settings import app_private_key_path, alipay_public_key_path
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderSerializer, \
    OrderDetailSerializer
from utils.alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能
    list: 获取购物车清单
    create: 加入购物车
    delete: 删除购物车中的商品
    update: 更新购物车商品
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    # serializer_class = ShoppingCartSerializer
    lookup_field = "goods_id"

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        exist_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = exist_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()


class OrderViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    订单管理
    list: 获取订单列表
    create: 生成订单
    delete: 删除订单
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)

        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            # 清空购物车
            shop_cart.delete()

        return order

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer


class AliPayViewSet(APIView):
    """阿里支付"""

    def get(self, request):
        """处理支付宝的return_url返回"""
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get("out_trade_no", None)
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("index")
            response.set_cookie("nextPath", "pay", max_age=2)

            return response
        else:
            response = redirect("index")
            return response

    def post(self, request):
        """处理支付宝的notify_url返回"""
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")
