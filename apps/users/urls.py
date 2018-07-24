# -*- coding: utf-8 -*-
'''
请写模块说明
'''
__author__ = "sunsn"
__date__ = '2018/7/22 15:41'

from django.conf.urls import url
from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView
from .views import UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView

urlpatterns = [
    # 用户信息
    url(r'info/$', UserinfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r'update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 用户个人中心修改邮箱时，发送邮箱验证码
    url(r'sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 用户个人中心修改邮箱
    url(r'update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 我收藏的课程讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
]