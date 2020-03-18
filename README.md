## 项目介绍

使用 `Vue+ Django REST framework` 前后端分离开发电商购物平台，实现功能主要包括：商品管理，手机注册及登录，用户收藏管理，订单管理，购物车管理，支付管理，后台管理等；



## 项目开发

### 后端开发环境

> Python：3.7
>
> Django：1.11.3
>
> djangorestframework：3.11.0		[文档](https://www.django-rest-framework.org/)
>
> 数据库：MySQL
>
> 后台管理：[xadmin](http://x.xuebingsi.com/)



### 项目初始化要点

将 `apps`，`extra_apps` 目录，加入到根搜索路径之下

```python
import sys
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
sys.path.insert(0,os.path.join(BASE_DIR, "extra_apps"))
```



### 模型

**注意：用户模型：**

- 继承自 `AbstractUser` ， 根据个人需求，添加所需字段

```python
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
```

- 替换系统用户：在 `settings.py` 中进行配置

```python
AUTH_USER_MODEL = "users.UserProfile"
```

- 外键父类指向自己，使用 `self`：

```python
parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录")
```

- 富文本编辑器配置

  > 1. `settings.py` 中配置 `INSTALLED_APPS`
  >
  >    ```python
  >    INSTALLED_APPS = [
  >        ...
  >        'DjangoUeditor',  # 富文本编辑器
  >        ...
  >    ]
  >    ```
  >
  > 2. 对应的 `models.py`
  >
  >    ```python
  >    from DjangoUeditor.models import UEditorField
  >    
  >    goods_desc = UEditorField(verbose_name=u"内容",imagePath="goods/images/", width=1000, height=300,filePath="goods/files/", default='')
  >    ```
  >
  >    

- 获取 `User` 模型的灵活方法

```python
from django.contrib.auth import get_user_model

User = get_user_model()
```

**注意：不要将 可视化工具管理数据库表 和 `makemigrations` 混合使用**



## `xadmin` 后台管理系统配置

1. 配置每个应用中的  `adminx.py` 文件

2. 安装相关依赖包：https://github.com/Leofighting/xadmin

   ```python
   django>=1.9.0
   django-crispy-forms>=1.6.0
   django-import-export>=0.5.1
   django-reversion>=2.0.0
   django-formtools==1.0
   future==0.15.2
   httplib2==0.9.2
   six==1.10.0
   django-guardian==1.4.9
   coreapi==2.3.1
   ```

3. 配置 `settings.py` 文件

> ```python
> INSTALLED_APPS = [
>     ...
>     'crispy_forms',
>     'xadmin',   # xadmin 后台管理系统
>     ...
> ]
> ```
>
> 

4. 生成迁移文件： `makemigrations --> migrate`

5. 配置反问路径，主目录下的 `urls.py`




## `Vue 与 RESTful API`

### 前后端分离

> 优点：
>
> 1. PC端、`APP`应用，移动端（手机、平板等） 多端适应
> 2. SPA（单页面应用） 开发模式的流行
> 3. 前后端开发职责不清晰
> 4. 开发效率问题，前后端互相等待
> 5. 前端配合后端，能力受限
> 6. 后台开发语言和模板高度耦合，导致开发语言依赖严重
>
> 缺点：
>
> 1. 前后端学习门槛增加
> 2. 数据依赖，导致文档重要性增加
> 3. 增加前端工作量
> 4. `SEO` 的难度增加
> 5. 后端开发模式迁移成本增加
>
> 

### `RESTful API`

> 前后端分离的最佳实践，规范
>
> 1. 轻量：直接通过`http`，不需要额外的协议，实现 post/get/put/delete 的操作
> 2. 面向资源，一目了然，具有自解析性
> 3. 数据描述简单，一般通过` json` 或者 `xml` 做数据通信
>
> 参考资料：
>
> 1. [理解RESTful架构](http://www.ruanyifeng.com/blog/2011/09/restful.html)
> 2. [RESTful API 设计指南](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)

### `Vue`

> 前端工程化
>
> 数据双向绑定
>
> 组件化开发

### `Django rest_framework API` 自动文档配置

> 主目录下 `ruls.py` :
>
> ```python
> from rest_framework.documentation import include_docs_urls
> 
> urlpatterns = [
>     ...
>     url(r"^docs/", include_docs_urls(title="your_project_name")),
>     url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
>     ...
> ]
> ```

> `settings.py` :
>
> ```python
> INSTALLED_APPS = [
>     ...
>     'rest_framework',
> ]
> ```



## `Django rest_framework API` 开发应用

### 序列化：针对 `json` 对象

> ```python
> from rest_framework import serializers
> 
> from goods.models import Goods, GoodsCategory
> 
> 
> class CategorySerializer(serializers.ModelSerializer):
>     """序列化：商品分类"""
> 
>     class Meta:
>         model = GoodsCategory
>         fields = "__all__"
> 
> 
> class GoodsSerializer(serializers.ModelSerializer):
>     """序列化：商品"""
>     category = CategorySerializer()  # 用序列化实例，覆盖原来的外键对象
> 
>     class Meta:
>         model = Goods
>         fields = "__all__"
> ```

### 视图 `views.py`

> ```python
> from rest_framework import mixins
> from rest_framework import viewsets
> 
> from goods.models import Goods
> from goods.serializers import GoodsSerializer
> 
> 
> class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
>     """
>     商品列表
>     """
>     queryset = Goods.objects.all()  # 模型
>     serializer_class = GoodsSerializer  # 序列化类
>     pagination_class = GoodsPagination  # 分页器类
> ```

### 路由 `urls.py`

> ```python
> from rest_framework.routers import DefaultRouter
> 
> from goods.views import GoodsListViewSet
> 
> router = DefaultRouter()
> 
> # 配置 商品列表 url
> router.register(r'goods', GoodsListViewSet)
> 
> 
> urlpatterns = [
>     ...
>     # router
>     url(r'^', include(router.urls)),
> ]
> ```

### 分页配置

> `settings.py`
>
> ```python
> REST_FRAMEWORK = {
>     'DEFAULT_PAGINATION_CLASS': "rest_framework.pagination.PageNumberPagination",  # 分页格式
>     "PAGE_SIZE": 10  # 每页显示数量
> }
> ```

> 定制分页器，对应`viewa.py` ：
>
> ```python
> from rest_framework.pagination import PageNumberPagination
> 
> 
> class GoodsPagination(PageNumberPagination):
>     page_size = 10  # 每页数量
>     page_size_query_param = 'page_size'  # 每页数量设置关键字
>     page_query_param = "p"  # 页数关键字
>     max_page_size = 100
> 
> 
> class GoodsListView(generics.ListAPIView):
>    ...
>     pagination_class = GoodsPagination
> ```

> 页面展示
>
> ![image-20200316180514355](E:\project\VueShop\MxShopV2\images\01.png)

### `APIView, GenericView, Viewset` 的逻辑关系

> 继承关系
>
> ```python
> View									# Django
> 	--APIView							# drf
>     	--GenericAPIView				# drf
>         	--GenericVieset(Viewset)	# drf
>             
> mixins
> 	CreateModelMixin
>     ListModelMixin
>     RetrieveModelMixin
>     UpdateModelMixin
>     DestroyModelMixin
> ```



### 过滤器

相关配置

> `settings.py`：
>
> ```python
> INSTALLED_APPS = [
>     ...
>     'django_filters',  
> ]
> 
> REST_FRAMEWORK = {
>     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
> }
> ```

> `views.py`：
>
> ```python
> from django_filters.rest_framework import DjangoFilterBackend
> 
> 
> class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
>     """
>     商品列表
>     """
>     ...
>     queryset = Goods.objects.all()
>     filter_backends = [DjangoFilterBackend]
>     filter_fields = ["name", "shop_price"]  # 注意，需要完全匹配才能得到过滤结果
> ```

> 页面效果
>
> ![image-20200316181834827](E:\project\VueShop\MxShopV2\images\02.png)

> 自定义过滤器
>
> `filters.py`
>
> ```python
> import django_filters
> 
> from goods.models import Goods
> 
> 
> class GoodsFilter(django_filters.rest_framework.FilterSet):
>     """自定义商品过滤器"""
>     price_min = django_filters.NumberFilter(name="shop_price", lookup_expr="gte")
>     price_max = django_filters.NumberFilter(name="shop_price", lookup_expr="lte")
> 
>     class Meta:
>         model = Goods
>         fields = ['price_min', 'price_max']
> ```
>
> `views.py`
>
> ```python
> from goods.filters import GoodsFilter
> 
> 
> class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
>     """
>     商品列表
>     """
>     ...
>     filter_class = GoodsFilter
> ```

### 模糊搜索

> ```python
> from rest_framework import filters
> 
> 
> class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
>     """
>     商品列表
>     """
> 	...
>     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
>     search_fields = ["name", "goods_brief", "goods_desc"]
> ```

> 页面效果
>
> ![image-20200316195713561](E:\project\VueShop\MxShopV2\images\03.png)

### 排序

> ```python
> class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
>     """
>     商品列表
>     """
> 	...
>     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
>     ordering_fields = ["sold_num", "add_time"]
> ```

> 页面效果
>
> ![image-20200316200535682](E:\project\VueShop\MxShopV2\images\04.png)

### 序列化多层嵌套

> ```python
> class CategorySerializer3(serializers.ModelSerializer):
>     """序列化：商品分类-二级"""
> 
>     class Meta:
>         model = GoodsCategory
>         fields = "__all__"
> 
> 
> class CategorySerializer2(serializers.ModelSerializer):
>     """序列化：商品分类-二级"""
>     sub_cat = CategorySerializer3(many=True)  # 三级分类的序列化
> 
>     class Meta:
>         model = GoodsCategory
>         fields = "__all__"
> 
> 
> class CategorySerializer(serializers.ModelSerializer):
>     """序列化：商品分类-一级"""
>     sub_cat = CategorySerializer2(many=True)  # 二级分类的序列化
> 
>     class Meta:
>         model = GoodsCategory
>         fields = "__all__"
> ```

### 处理跨域访问问题

> [相关文档](https://github.com/Leofighting/django-cors-headers)
>
> `settings.py` 配置
>
> ```python
> INSTALLED_APPS = [
>     ...
>     'corsheaders',
>     ...
> ]
> 
> MIDDLEWARE = [
>     ...
>     'corsheaders.middleware.CorsMiddleware',  # 尽量放前面
>     ...
> ]
> 
> # django-cors-headers 配置
> CORS_ORIGIN_ALLOW_ALL = True
> 
> ```



## 用户登录

前后端分离的用户系统，常用 `TokenAuthentication`

> 配置 `settings.py`
>
> ```python
> INSTALLED_APPS = [
>     ...
>     'rest_framework.authtoken'
> ]
> 
> REST_FRAMEWORK = {
>     'DEFAULT_AUTHENTICATION_CLASSES': [
>         'rest_framework.authentication.BasicAuthentication',
>         'rest_framework.authentication.SessionAuthentication',
>         'rest_framework.authentication.TokenAuthentication',
>     ]
> }
> ```

> 生成数据迁移表

> 主目录下的`urls.py`
>
> ```python
> from rest_framework.authtoken import views
> urlpatterns += [
>     url(r'^api-token-auth/', views.obtain_auth_token)
> ]
> ```

> 仅在接口处进行用户验证，需要删除 `settings.py` 中的全局配置
>
> 在 `views.py` 中配置
>
> ```python
> from rest_framework.authentication import TokenAuthentication
> 
> 
> class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
>     """
>     商品列表
>     """
>     ...
>     authentication_classes = [TokenAuthentication]
> ```

> 公开数据，不需要做用户验证，可以游客身份浏览公开页面

### `JWT` 用户认证

> 参考资料：[前后端分离之JWT用户认证](https://lion1ou.win/2017/01/18/)
>
> 使用安装包 ：[django-rest-framework-jwt](https://github.com/Leofighting/django-rest-framework-jwt)；[官方文档](http://jpadilla.github.io/django-rest-framework-jwt/)

> 安装：`pip install djangorestframework-jwt`

> 配置：
>
> `settings.py`
>
> ```python
> REST_FRAMEWORK = {
>     'DEFAULT_AUTHENTICATION_CLASSES': (
>         ...
>         'rest_framework.authentication.BasicAuthentication',
>     ),
> }
> 
> # JWT 设置
> JWT_AUTH = {
>     'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),  # 设置过期时间
>     'JWT_AUTH_HEADER_PREFIX': 'JWT',  # 验证方式
> }
> ```
>
> `urls.py`
>
> ```python
> from rest_framework_jwt.views import obtain_jwt_token
> #...
> 
> urlpatterns = [
>     '',
>     # ...
> 
>     url(r'^api-token-auth/', obtain_jwt_token),
> ]
> ```



## 用户注册

> 短信验证第三方服务：[云片网](https://www.yunpian.com/)      [官方文档](https://www.yunpian.com/official/document/sms/zh_CN/readme)

> 用户前端页面提交的数据都储存在 `initial_data` 属性中，可在序列化时提取验证
>
> ```python
> class UserSerializer(serializers.ModelSerializer):
>     """序列化：用户"""
>     code = serializers.CharField(required=True, max_length=4, min_length=4)
>     
>     def validate_code(self, code):
>         """核对验证码"""
>         verify_record = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
> ```

> 删除前端输入的，无需保存在数据库中的参数，例如用户输入的验证码，只需用于核对，无需储存在数据库中
>
> 在序列化中做数据校验
>
> ```python
> def validate(self, attrs):
>     attrs["mobile"] = attrs["username"]  # 将用户前端输入的用户名赋值作为手机号码
>     del attrs["code"]  # 删除前端提交的验证码
>     return attrs
> ```

> 验证用户名的唯一性
>
> ```python
> from rest_framework.validators import UniqueValidator
> 
> username = serializers.CharField(required=True, allow_blank=False,
>                                      validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在~")])
> ```

> `write_only=True`
>
> ```python
> # 序列化时，会忽略 code 字段
> code = serializers.CharField(required=True, max_length=4, min_length=4, 
>                              write_only=True, help_text="请输入验证码", label="验证码")
> ```

> ```python
> # 设置密码为密文形式
> password = serializers.CharField(
>     style={'input_type': 'password'}
> )
> ```

### 信号量机制

> `Django` 会对请求、提交、删除等操作时发出的信号进行捕捉，捕捉信号后，可以在其中加入相应的操作逻辑；代码分离性好
>
> [相关文档](https://docs.djangoproject.com/en/1.10/ref/signals/)

> 在对应的应用下创建 `signals.py`
>
> ```python
> from django.db.models.signals import post_save
> from django.dispatch import receiver
> from django.contrib.auth import get_user_model
> 
> User = get_user_model()
> 
> 
> @receiver(post_save, sender=User)
> def create_auth_token(sender, instance=None, created=False, **kwargs):
>     if created:
>         password = instance.password
>         instance.set_password(password)
>         instance.save()
> ```

> 在 `apps.py` 文件中配置
>
> ```python
> from django.apps import AppConfig
> 
> 
> class UsersConfig(AppConfig):
>     name = 'apps.users'
>     verbose_name = "用户管理"
> 
>     def ready(self):
>         import users.signals  # 导入信号量模块
> ```