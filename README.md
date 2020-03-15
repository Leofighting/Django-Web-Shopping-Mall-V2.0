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

