# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm


# Create your views here.
class CustomBackend(ModelBackend):
    """
    自定义登录类，实现邮箱和用户名都可以登录
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # UserProfile继承自AbstractUser
            # 这个Q,|表示或or，“,”表示并and
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # AbstractUser有一个方法验证传入的密码是否正确，数据库里是密文
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 一般来说，教程里是函数，但是django其实更推荐类来实现view功能
def user_login(request):
    """
    废弃， 今后都用类来完成，对应本函数的类是LoginView
    :param request:
    :return:
    """
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")

        # 在settings.py配置AUTHENTICATION_BACKENDS后，
        # authenticate会自动跳转到我们定义的CustomBackend类中
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误"})
    elif request.method == "GET":
        return render(request, "login.html", {})


class LoginView(View):
    """登录类"""
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # LoginForm需要一个字典变量，request.POST可以传进去
        # 但LoginForm里定义的变量名，必须和前端传进来的变量名一致
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 在settings.py配置AUTHENTICATION_BACKENDS后，
            # authenticate会自动跳转到我们定义的CustomBackend类中
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, "index.html")
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})




