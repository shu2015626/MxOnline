# -*- coding: utf-8 -*-
'''
请写模块说明
'''
__author__ = "sunsn"
__date__ = '2018/7/22 15:41'

from django.conf.urls import url
from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView
from .views import UpdateEmailView

urlpatterns = [
    # 用户信息
    url(r'info/$', UserinfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r'update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 修改邮箱时，发送邮箱验证码
    url(r'sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    url(r'update_email/$', UpdateEmailView.as_view(), name='update_email'),
]