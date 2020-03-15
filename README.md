## 项目介绍

使用 `Vue+ Django REST framework` 前后端分离开发电商购物平台，实现功能主要包括：商品管理，手机注册及登录，用户收藏管理，订单管理，购物车管理，支付管理，后台管理等；

### 后端开发环境

> Python：3.7
>
> Django：1.11.3
>
> djangorestframework：3.11.0
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

