from random import choice

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from MxShopV2.settings import API_KEY
from users.models import VerifyCode
from users.serializers import SmsSerializer, UserRegisterSerializer
from utils.yunpian import YunPian

User = get_user_model()


class CustomBackend(ModelBackend):
    """自定义用户验证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """短信验证码"""
    serializer_class = SmsSerializer

    @staticmethod
    def generate_code():
        """生成4位数字验证码"""
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        """重写create() 方法"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        code = self.generate_code()

        # 使用云片网发送短信验证码
        # yunpian = YunPian(API_KEY)
        # sms_status = yunpian.send_sms(code=code, mobile=mobile)
        #
        # if sms_status["code"] != 0:
        #     return Response({
        #         "mobile": sms_status["msg"]
        #     }, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     code_record = VerifyCode(code=code, mobile=mobile)
        #     code_record.save()
        #     return Response({
        #         "mobile": mobile
        #     }, status=status.HTTP_201_CREATED)

        # 不使用云片网,直接输出验证码
        VerifyCode.objects.create(code=code, mobile=mobile)
        print("验证码是：", code)
        return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """用户"""
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name or user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()