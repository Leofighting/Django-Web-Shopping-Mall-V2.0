# -*- coding:utf-8 -*-
__author__ = "leo"

import re
from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from MxShopV2.settings import REGEX_MOBILE
from users.models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """序列化：短信验证码"""
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """验证手机号码"""
        # 是否已注册
        if User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError("该手机号码已被注册~")

        # 手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("该手机号码不合法~")

        # 验证发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)

        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile):
            raise serializers.ValidationError("一分钟内只能发送一次验证码~")

        return mobile


class UserRegisterSerializer(serializers.ModelSerializer):
    """序列化：用户"""
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 write_only=True, help_text="请输入验证码", label="验证码")

    username = serializers.CharField(required=True, allow_blank=False,
                                     label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在~")])

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="密码"
    )

    # def create(self, validated_data):
    #     user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        """核对验证码"""
        verify_record = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")

        if verify_record:
            last_record = verify_record[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=10, seconds=0)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码已失效~")

            if last_record.code != code:
                raise serializers.ValidationError("请输入正确的验证码~")

        else:
            raise serializers.ValidationError("验证码错误~")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ["username", "code", "mobile", "password"]


class UserDetailSerializer(serializers.ModelSerializer):
    """序列化：用户详情"""
    class Meta:
        model = User
        fields = ["name", "gender", "birthday", "email", "mobile"]