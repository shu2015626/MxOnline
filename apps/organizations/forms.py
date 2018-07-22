# -*- coding: utf-8 -*-
'''
请写模块说明
'''
__author__ = "sunsn"
__date__ = '2018/7/11 21:40'
import re
from django import forms
from operation.models import UserAsk

'''
class UserAskForm(forms.Form):
    """之前定义的Form"""
    name = forms.CharField(required=True, min_length=2, max_length=20)
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    course_name = forms.CharField(required=True, min_length=5, max_length=50)


class AnotherUserAskForm(forms.ModelForm):
    """通过model生成的ModelForm"""
    # my_filed = forms.CharField()  # 在使用model转化为form的基础上，还可以增加自定义字段
    class Meta:
        model = UserAsk  # 使用哪个model转化为form
        fields = ['name', 'mobile', 'course_name']  # 需要将哪些字段转化为form
'''


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 重写我们的字段验证方法，而不是使用默认的函数
    def clean_mobile(self):
        """
        验证手机号码是否合法

        对我们的字段进行验证，
        必须使用clean开通，以下划线分割加上我们的字段名
        :return:
        """
        # ModelForm内置的变量：dict
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")

