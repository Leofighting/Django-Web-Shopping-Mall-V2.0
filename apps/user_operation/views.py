from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, \
    AddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户收藏
    list: 获取用户收藏列表
    create: 添加用户收藏
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavViewSet

        return UserFavViewSet


class LeavingMessageViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,
                            mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    用户留言板
    list: 获取用户留言
    create: 添加留言
    delete: 删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    """
    用户地址
    list: 获取收货地址列表
    create: 添加收货地址
    update: 更新收货地址
    delete: 删除收货地址
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
