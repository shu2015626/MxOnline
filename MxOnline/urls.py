# -*- coding: utf-8 -*-
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve

from users.views import (LoginView, RegisterView, ActiveUserView, ForgetPwdView,
                         ResetView, ModifyPwdView, LogoutView, IndexView)
# from users.views import user_login, LoginUnsafeView
from organizations.views import OrgView
from MxOnline.settings import MEDIA_ROOT
# from MxOnline.settings import STATIC_ROOT

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    # url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('^$', IndexView.as_view(), name="index"),
    # url('^login/$', TemplateView.as_view(template_name="login.html"), name="login"),
    # url('^login/$', user_login, name="login"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url('^login/$', LoginView.as_view(), name="login"),
    # url('^login/$', LoginUnsafeView.as_view(), name="login"),

    url('^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构url配置
    url(r'^org/', include('organizations.urls', namespace="org")),

    # 课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),

    # 配置上传文件的访问处理函数（专门处理media的信息）
    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 用户相关url配置
    url(r'user/', include('users.urls', namespace='user')),

    # url(r'static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 配置ueditor-->富文本相关url
    url(r'^ueditor/',include('DjangoUeditor.urls' ))

]


# 全局404和500页面配置
handler404 = "users.views.page_not_found"
handler500 = "users.views.page_error"