"""MxShopV2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from MxShopV2.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, HotSearchesViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet, AliPayViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from users.views import SmsCodeViewSet, UserViewSet

router = DefaultRouter()

# 配置 商品列表 url
router.register(r'goods', GoodsListViewSet, basename="goods")
# 配置 商品分类列表 url
router.register(r'categorys', CategoryViewSet, basename="categorys")
# 配置 短信验证码 url
router.register(r'code', SmsCodeViewSet, basename="code")
# 配置 热搜词 url
router.register(r'hotsearchs', HotSearchesViewSet, basename="hotsearchs")
# 配置 用户 url
router.register(r'users', UserViewSet, basename="users")
# 配置 用户收藏 url
router.register(r'userfavs', UserFavViewSet, basename="userfavs")
# 配置 用户留言 url
router.register(r'messages', LeavingMessageViewSet, basename="messages")
# 配置 用户地址 url
router.register(r'address', AddressViewSet, basename="address")
# 配置 购物车 url
router.register(r'shopcarts', ShoppingCartViewSet, basename="shopcarts")
# 配置 订单 url
router.register(r'orders', OrderViewSet, basename="orders")

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r"^media/(?P<path>.*)$", serve, {"document_root": MEDIA_ROOT}),
    # 文档
    url(r"^docs/", include_docs_urls(title="慕学生鲜")),
    # api 接口
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # router
    url(r'^', include(router.urls)),
    # 用户登录 drf 自带的Token 认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt 认证接口
    url(r'^login/', obtain_jwt_token),
    # 阿里支付接口
    url(r'^alipay/return/', AliPayViewSet, name="alipay"),
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
]
