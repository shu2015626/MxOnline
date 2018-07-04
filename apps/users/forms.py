# -*- coding: utf-8 -*-
'''
定义forms来进行表单的验证
'''
__author__ = "sunsn"
__date__ = '2018/7/3 22:55'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)